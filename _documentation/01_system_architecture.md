# Ollama Deep Researcher - System Architecture

## Overview
The Ollama Deep Researcher is built on LangGraph, implementing an iterative research workflow that combines local LLM capabilities with web search to perform deep research on given topics.

## Core Components

### 1. Configuration Management (`configuration.py`)
- Manages configurable parameters through the `Configuration` class
- Key parameters:
  - `max_web_research_loops`: Controls depth of research iterations
  - `local_llm`: Specifies which Ollama model to use
- Supports environment variable and runtime configuration

### 2. State Management (`state.py`)
- Uses `SummaryState` dataclass to track research progress
- Key state elements:
  - `research_topic`: Initial research topic
  - `search_query`: Current search query
  - `web_research_results`: Accumulated research results
  - `sources_gathered`: List of sources used
  - `research_loop_count`: Iteration counter
  - `running_summary`: Current research summary

### 3. LLM Prompts (`prompts.py`)
Three core prompt templates:
1. `query_writer_instructions`: Generates web search queries
2. `summarizer_instructions`: Creates/extends research summaries
3. `reflection_instructions`: Identifies knowledge gaps

### 4. Research Graph (`graph.py`)
Implements the core research workflow using LangGraph:

#### Nodes:
1. `generate_query`: Creates initial search query
2. `web_research`: Performs web search via Tavily
3. `summarize_sources`: Synthesizes search results
4. `reflect_on_summary`: Analyzes gaps and generates follow-up queries
5. `finalize_summary`: Formats final output with sources

#### Flow:
```
START
  → generate_query
  → web_research
  → summarize_sources
  → reflect_on_summary
  → [conditional: web_research OR finalize_summary]
  → END
```

### 5. Utilities (`utils.py`)
Core utility functions:
- `tavily_search`: Web search integration
- `deduplicate_and_format_sources`: Source processing
- `format_sources`: Output formatting

## External Dependencies
1. Ollama
   - Local LLM hosting
   - Used for all LLM operations

2. Tavily
   - Web search API
   - Provides search results with content extraction

3. LangGraph
   - Workflow orchestration
   - State management
   - Conditional routing

## Data Flow

### Research Iteration
1. Initial Query Generation
   - Input: Research topic
   - Output: Search query + metadata

2. Web Research
   - Input: Search query
   - Output: Search results + raw content

3. Summarization
   - Input: Search results + existing summary
   - Output: Updated summary

4. Reflection
   - Input: Current summary
   - Output: Knowledge gaps + follow-up query

### State Transitions
- State is maintained across iterations
- Sources are accumulated
- Summary is incrementally updated
- Research depth is tracked
