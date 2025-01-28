"""LangGraph-based research assistant that performs iterative web research.

This module implements a state machine for conducting research using LangGraph.
It includes nodes for query generation, web research, summarization, and reflection.
The graph maintains state between iterations and can perform multiple research loops
to gather comprehensive information on a topic."""

import json
import os
import sys
import time
from typing_extensions import Literal

from langgraph.graph import START, END, StateGraph
from langchain_core.runnables import RunnableConfig
from openai import OpenAI

from assistant.configuration import Configuration
from assistant.prompts import (
    query_writer_instructions,
    summarizer_instructions,
    reflection_instructions
)
from assistant.state import SummaryState, SummaryStateInput, SummaryStateOutput
from assistant.utils import (
    deduplicate_and_format_sources,
    format_sources,
    tavily_search
)

def write_console(message: str) -> None:
    """Write a message to the console with proper encoding.
    
    Args:
        message: The message to write.
    """
    try:
        # Try writing directly first
        if sys.stdout is None or sys.stdout.closed:
            return  # Silently ignore if stdout is not available
        sys.stdout.write(message)
        sys.stdout.flush()
    except (UnicodeEncodeError, OSError) as e:
        try:
            # If that fails, encode as UTF-8 and decode with console encoding
            if sys.stdout is None or sys.stdout.buffer is None or sys.stdout.closed:
                return  # Silently ignore if stdout is not available
            if sys.platform == 'win32':
                # Force UTF-8 for Windows console
                sys.stdout.buffer.write(message.encode('utf-8'))
                sys.stdout.buffer.flush()
            else:
                # For other platforms, try console encoding
                encoding = sys.stdout.encoding or 'utf-8'
                sys.stdout.buffer.write(message.encode(encoding, errors='replace'))
                sys.stdout.buffer.flush()
        except (OSError, AttributeError):
            pass  # Silently ignore if we can't write to stdout

def generate_query(state: SummaryState, config: RunnableConfig) -> dict:
    """Generate a search query based on the research topic.
    
    Args:
        state: Current state containing research topic and history.
        config: Configuration for the query generation.
        
    Returns:
        dict: Contains the generated search query.
        
    Raises:
        ValueError: If the API response is invalid or empty.
    """
    try:
        # Validate state
        if not state or not state.research_topic:
            raise ValueError("Research topic is required but was not provided")
            
        write_console("\n🔍 Generating search query...\n")
        start_time = time.time()
    
        # Format the prompt
        query_writer_instructions_formatted = query_writer_instructions.format(
            research_topic=state.research_topic
        )

        # Initialize DeepSeek client
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable is not set")
            
        chat_client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )

        # Generate a query using DeepSeek
        configurable = Configuration.from_runnable_config(config)
        if not configurable or not configurable.model:
            raise ValueError("Model configuration is missing")
            
        write_console(f"Using model: {configurable.model}\n")
        write_console("Making API request to DeepSeek...\n")
        
        try:
            response = chat_client.chat.completions.create(
                model=configurable.model,
                messages=[
                    {"role": "system", "content": query_writer_instructions_formatted},
                    {"role": "user", "content": "Generate a query for web search:"}
                ],
                response_format={"type": "json_object"}
            )
            write_console("✅ API request successful\n")
        except Exception as e:
            write_console(f"❌ API request failed: {str(e)}\n")
            if hasattr(e, 'response'):
                write_console(f"Response status: {e.response.status_code}\n")
                write_console(f"Response body: {e.response.text}\n")
            raise ValueError(f"DeepSeek API request failed: {str(e)}")
        
        # Safely parse JSON response with type checking
        content = response.choices[0].message.content
        write_console(f"Raw API response: {content}\n")
        
        if not content or not content.strip():
            raise ValueError("Empty response from DeepSeek API")
            
        try:
            query_data = json.loads(content)
            if not isinstance(query_data, dict) or 'query' not in query_data:
                raise ValueError("Invalid response format")
            query = query_data['query']
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {e}")
        
        duration = time.time() - start_time
        write_console(f"✅ Query generated in {duration:.2f}s: {query}\n")
        
        return {"search_query": query}
        
    except Exception as e:
        write_console(f"❌ Error generating query: {str(e)}\n")
        raise

def web_research(state: SummaryState) -> dict:
    """Perform web research using the generated query.
    
    Args:
        state: Current state containing the search query.
        
    Returns:
        dict: Contains the research results.
    """
    try:
        # Validate state
        if not state or not state.search_query:
            raise ValueError("Search query is required but was not provided")
            
        write_console("\n🌐 Performing web research...\n")
        start_time = time.time()
    
        # Search the web
        search_results = tavily_search(state.search_query, include_raw_content=True, max_results=1)
        
        # Format the sources
        search_str = deduplicate_and_format_sources(search_results, max_tokens_per_source=1000)
        
        duration = time.time() - start_time
        write_console(f"✅ Web search completed in {duration:.2f}s\n")
        
        return {"sources_gathered": [format_sources(search_results)], 
                "research_loop_count": state.research_loop_count + 1, 
                "web_research_results": [search_str]}
                
    except Exception as e:
        write_console(f"❌ Error in web search: {str(e)}\n")
        raise

def summarize_sources(state: SummaryState, config: RunnableConfig) -> dict:
    """Summarize the gathered research sources.
    
    Args:
        state: Current state containing sources to summarize.
        config: Configuration for the summarization.
        
    Returns:
        dict: Contains the generated summary.
        
    Raises:
        ValueError: If the API response is invalid or empty.
    """
    try:
        # Validate state
        if not state or not state.sources_gathered:
            raise ValueError("Sources are required but were not provided")
            
        write_console("\n📝 Summarizing sources...\n")
        start_time = time.time()
    
        # Get the current summary and sources
        running_summary = state.running_summary or ""  # Default to empty string if None
        sources = state.sources_gathered or []  # Default to empty list if None
        
        if not sources:
            write_console("No sources to summarize\n")
            return {}
            
        # Format sources for the prompt
        formatted_sources = format_sources(sources)
        summarizer_instructions_formatted = summarizer_instructions.format(
            research_topic=state.research_topic,
            sources=formatted_sources,
            current_summary=running_summary
        )
        
        # Initialize DeepSeek client
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable is not set")
            
        chat_client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )
        
        # Generate summary using DeepSeek
        configurable = Configuration.from_runnable_config(config)
        if not configurable or not configurable.model:
            raise ValueError("Model configuration is missing")
            
        response = chat_client.chat.completions.create(
            model=configurable.model,
            messages=[
                {"role": "system", "content": summarizer_instructions_formatted},
                {"role": "user", "content": "Please summarize the sources:"}
            ],
            response_format={"type": "json_object"}
        )
        
        # Safely parse JSON response
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from DeepSeek API")
            
        try:
            summary_data = json.loads(content)
            if not isinstance(summary_data, dict) or 'summary' not in summary_data:
                raise ValueError("Invalid response format")
            running_summary = summary_data['summary']
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {e}")

        # Remove think tags if present using string operations with proper checks
        if running_summary and isinstance(running_summary, str):
            while True:
                start_tag = "<think>"
                end_tag = "</think>"
                start_idx = running_summary.find(start_tag)
                end_idx = running_summary.find(end_tag)
                
                if start_idx == -1 or end_idx == -1:
                    break
                    
                # Calculate the end position including the end tag
                end_pos = end_idx + len(end_tag)
                if end_pos <= len(running_summary):
                    running_summary = running_summary[:start_idx] + running_summary[end_pos:]
                else:
                    break

        duration = time.time() - start_time
        write_console(f"✅ Summary generated in {duration:.2f}s\n")
        
        return {"running_summary": running_summary}
        
    except Exception as e:
        write_console(f"❌ Error summarizing sources: {str(e)}\n")
        raise

def reflect_on_summary(state: SummaryState, config: RunnableConfig) -> dict:
    """Reflect on the current summary and decide if more research is needed.
    
    Args:
        state: Current state containing the summary to reflect on.
        config: Configuration for the reflection.
        
    Returns:
        dict: Contains reflection results and potential follow-up query.
        
    Raises:
        ValueError: If the API response is invalid or empty.
    """
    try:
        # Validate state
        if not state or not state.running_summary:
            raise ValueError("Summary is required but was not provided")
            
        write_console("\n🤔 Reflecting on summary...\n")
        start_time = time.time()
    
        # Get the current summary
        running_summary = state.running_summary or ""  # Default to empty string if None
        
        if not running_summary:
            write_console("No summary to reflect on\n")
            return {"should_continue": False}
            
        # Format the prompt
        reflection_instructions_formatted = reflection_instructions.format(
            research_topic=state.research_topic,
            current_summary=running_summary
        )

        # Initialize DeepSeek client
        api_key = os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY environment variable is not set")
            
        chat_client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )

        # Generate reflection using DeepSeek
        configurable = Configuration.from_runnable_config(config)
        if not configurable or not configurable.model:
            raise ValueError("Model configuration is missing")
            
        response = chat_client.chat.completions.create(
            model=configurable.model,
            messages=[
                {"role": "system", "content": reflection_instructions_formatted},
                {"role": "user", "content": "Please reflect on the current summary:"}
            ],
            response_format={"type": "json_object"}
        )
        
        # Safely parse JSON response
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from DeepSeek API")
            
        try:
            reflection_data = json.loads(content)
            if not isinstance(reflection_data, dict):
                raise ValueError("Invalid response format")
                
            should_continue = reflection_data.get('should_continue', False)
            if not isinstance(should_continue, bool):
                should_continue = False  # Default to False if invalid
                
            follow_up_query = reflection_data.get('follow_up_query', '')
            if not isinstance(follow_up_query, str):
                follow_up_query = ''  # Default to empty string if invalid
                
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {e}")

        duration = time.time() - start_time
        write_console(f"✅ Reflection generated in {duration:.2f}s\n")
        
        return {
            "should_continue": should_continue,
            "follow_up_query": follow_up_query
        }
        
    except Exception as e:
        write_console(f"❌ Error generating reflection: {str(e)}\n")
        raise

def finalize_summary(state: SummaryState) -> dict:
    """Finalize the research summary.
    
    Args:
        state: Current state containing the final summary.
        
    Returns:
        dict: Contains the finalized summary.
    """
    try:
        # Validate state
        if not state or not state.running_summary:
            raise ValueError("Summary is required but was not provided")
            
        # Format all accumulated sources into a single bulleted list
        all_sources = "\n".join(source for source in state.sources_gathered)
        state.running_summary = f"## Summary\n\n{state.running_summary}\n\n ### Sources:\n{all_sources}"
        return {"running_summary": state.running_summary}
        
    except Exception as e:
        write_console(f"❌ Error finalizing summary: {str(e)}\n")
        raise

def route_research(state: SummaryState) -> Literal["generate_query", "finalize_summary"]:
    """Determine whether to continue research or end.
    
    Args:
        state: Current state containing research progress.
        
    Returns:
        Literal["generate_query", "finalize_summary"]: Next node to route to.
    """
    try:
        # Validate state
        if not state:
            raise ValueError("State is required but was not provided")
            
        if not hasattr(state, 'research_loop_count'):
            raise ValueError("Research loop count is missing from state")
            
        # Use default max loops if not set
        max_loops = getattr(state, 'max_research_loops', 3)
            
        if state.research_loop_count >= max_loops:
            write_console(f"\n📊 Reached maximum research loops ({max_loops}), finalizing summary...\n")
            return "finalize_summary"
            
        write_console(f"\n🔄 Research loop {state.research_loop_count + 1}/{max_loops}, continuing research...\n")
        return "generate_query"
        
    except Exception as e:
        write_console(f"❌ Error routing research: {str(e)}\n")
        raise

# Build the graph
builder = StateGraph(SummaryState, input=SummaryStateInput, output=SummaryStateOutput, config_schema=Configuration)

# Add nodes
builder.add_node("generate_query", generate_query)
builder.add_node("web_research", web_research)
builder.add_node("summarize_sources", summarize_sources)
builder.add_node("reflect_on_summary", reflect_on_summary)
builder.add_node("finalize_summary", finalize_summary)

# Add edges
builder.add_edge("generate_query", "web_research")
builder.add_edge("web_research", "summarize_sources")
builder.add_edge("summarize_sources", "reflect_on_summary")

# Add conditional edge from reflect_on_summary
builder.add_conditional_edges(
    "reflect_on_summary",  # Source node
    route_research  # Function that returns the next node name
)

# Set entry and exit
builder.set_entry_point("generate_query")
builder.set_finish_point("finalize_summary")

# Create the graph
graph = builder.compile()