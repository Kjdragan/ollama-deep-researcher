import json
import os
import time
from typing_extensions import Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from openai import OpenAI
from langgraph.graph import START, END, StateGraph

from assistant.configuration import Configuration
from assistant.utils import deduplicate_and_format_sources, tavily_search, format_sources
from assistant.state import SummaryState, SummaryStateInput, SummaryStateOutput
from assistant.prompts import query_writer_instructions, summarizer_instructions, reflection_instructions

# Nodes   
def generate_query(state: SummaryState, config: RunnableConfig):
    """ Generate a query for web search """
    
    print("\n🔍 Generating search query...")
    start_time = time.time()
    
    try:
        # Format the prompt
        query_writer_instructions_formatted = query_writer_instructions.format(research_topic=state.research_topic)

        # Initialize DeepSeek client
        chat_client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com/v1"
        )

        # Generate a query using DeepSeek
        configurable = Configuration.from_runnable_config(config)
        response = chat_client.chat.completions.create(
            model=configurable.model,
            messages=[
                {"role": "system", "content": query_writer_instructions_formatted},
                {"role": "user", "content": "Generate a query for web search:"}
            ],
            response_format={"type": "json_object"}
        )
        query = json.loads(response.choices[0].message.content)
        
        duration = time.time() - start_time
        print(f"✅ Query generated in {duration:.2f}s: {query['query']}")
        
        return {"search_query": query['query']}
        
    except Exception as e:
        print(f"❌ Error generating query after {time.time() - start_time:.2f}s: {str(e)}")
        raise

def web_research(state: SummaryState):
    """ Gather information from the web """
    
    print("\n🌐 Searching the web...")
    start_time = time.time()
    
    try:
        # Search the web
        search_results = tavily_search(state.search_query, include_raw_content=True, max_results=1)
        
        # Format the sources
        search_str = deduplicate_and_format_sources(search_results, max_tokens_per_source=1000)
        
        duration = time.time() - start_time
        print(f"✅ Web search completed in {duration:.2f}s")
        
        return {"sources_gathered": [format_sources(search_results)], 
                "research_loop_count": state.research_loop_count + 1, 
                "web_research_results": [search_str]}
                
    except Exception as e:
        print(f"❌ Error in web search after {time.time() - start_time:.2f}s: {str(e)}")
        raise

def summarize_sources(state: SummaryState, config: RunnableConfig):
    """ Summarize the gathered sources """
    
    print("\n📝 Summarizing sources...")
    start_time = time.time()
    
    try:
        # Existing summary
        existing_summary = state.running_summary

        # Most recent web research
        most_recent_web_research = state.web_research_results[-1]

        # Build the human message
        if existing_summary:
            human_message_content = (
                f"Extend the existing summary: {existing_summary}\n\n"
                f"Include new search results: {most_recent_web_research} "
                f"That addresses the following topic: {state.research_topic}"
            )
        else:
            human_message_content = (
                f"Generate a summary of these search results: {most_recent_web_research} "
                f"That addresses the following topic: {state.research_topic}"
            )

        # Initialize DeepSeek client
        chat_client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com/v1"
        )

        # Run the LLM
        configurable = Configuration.from_runnable_config(config)
        response = chat_client.chat.completions.create(
            model=configurable.model,
            messages=[
                {"role": "system", "content": summarizer_instructions},
                {"role": "user", "content": human_message_content}
            ],
            response_format={"type": "text"}
        )
        running_summary = response.choices[0].message.content

        # TODO: This is a hack to remove the <think> tags w/ Deepseek models 
        # It appears very challenging to prompt them out of the responses 
        while "<think>" in running_summary and "</think>" in running_summary:
            start = running_summary.find("<think>")
            end = running_summary.find("</think>") + len("</think>")
            running_summary = running_summary[:start] + running_summary[end:]

        duration = time.time() - start_time
        print(f"✅ Summary generated in {duration:.2f}s")
        
        return {"running_summary": running_summary}
        
    except Exception as e:
        print(f"❌ Error generating summary after {time.time() - start_time:.2f}s: {str(e)}")
        raise

def reflect_on_summary(state: SummaryState, config: RunnableConfig):
    """ Reflect on the summary and generate a follow-up query """

    print("\n🤔 Reflecting on summary...")
    start_time = time.time()
    
    try:
        # Initialize DeepSeek client
        chat_client = OpenAI(
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com/v1"
        )

        # Generate a query using DeepSeek
        configurable = Configuration.from_runnable_config(config)
        response = chat_client.chat.completions.create(
            model=configurable.model,
            messages=[
                {"role": "system", "content": reflection_instructions.format(research_topic=state.research_topic)},
                {"role": "user", "content": f"Identify a knowledge gap and generate a follow-up web search query based on our existing knowledge: {state.running_summary}"}
            ],
            response_format={"type": "json_object"}
        )
        follow_up_query = json.loads(response.choices[0].message.content)

        duration = time.time() - start_time
        print(f"✅ Follow-up query generated in {duration:.2f}s: {follow_up_query['follow_up_query']}")
        
        return {"search_query": follow_up_query['follow_up_query']}
        
    except Exception as e:
        print(f"❌ Error generating follow-up query after {time.time() - start_time:.2f}s: {str(e)}")
        raise

def finalize_summary(state: SummaryState):
    """ Finalize the summary """
    
    # Format all accumulated sources into a single bulleted list
    all_sources = "\n".join(source for source in state.sources_gathered)
    state.running_summary = f"## Summary\n\n{state.running_summary}\n\n ### Sources:\n{all_sources}"
    return {"running_summary": state.running_summary}

def route_research(state: SummaryState, config: RunnableConfig) -> Literal["finalize_summary", "web_research"]:
    """ Route the research based on the follow-up query """

    configurable = Configuration.from_runnable_config(config)
    if state.research_loop_count <= configurable.max_web_research_loops:
        return "web_research"
    else:
        return "finalize_summary" 
    
# Add nodes and edges 
builder = StateGraph(SummaryState, input=SummaryStateInput, output=SummaryStateOutput, config_schema=Configuration)
builder.add_node("generate_query", generate_query)
builder.add_node("web_research", web_research)
builder.add_node("summarize_sources", summarize_sources)
builder.add_node("reflect_on_summary", reflect_on_summary)
builder.add_node("finalize_summary", finalize_summary)

# Add edges
builder.add_edge(START, "generate_query")
builder.add_edge("generate_query", "web_research")
builder.add_edge("web_research", "summarize_sources")
builder.add_edge("summarize_sources", "reflect_on_summary")
builder.add_conditional_edges("reflect_on_summary", route_research)
builder.add_edge("finalize_summary", END)

graph = builder.compile()