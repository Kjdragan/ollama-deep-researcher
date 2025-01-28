# Ollama Deep Researcher - Technical Analysis

## Project Overview
The Ollama Deep Researcher is a local web research assistant that leverages local LLMs through Ollama to perform iterative web research. The project implements an iterative research methodology inspired by IterDRAG.

## Project Structure
```
src/assistant/
├── __init__.py
├── configuration.py  - Configuration management
├── graph.py         - Core LangGraph implementation
├── prompts.py       - LLM prompt templates
├── state.py        - State management
└── utils.py        - Utility functions
```

## Core Components
1. LangGraph Integration
   - Uses LangGraph for workflow orchestration
   - Implements an iterative research process
   - Manages state across research iterations

2. External Services
   - Ollama: Local LLM hosting
   - Tavily: Web search API (configurable)

3. Research Workflow
   - Query Generation
   - Web Search
   - Result Summarization
   - Gap Analysis
   - Iterative Refinement

## Next Analysis Steps
1. [ ] Analyze configuration management
2. [ ] Document LangGraph implementation
3. [ ] Review prompt templates
4. [ ] Examine state management
5. [ ] Study utility functions
6. [ ] Map data flow between components
7. [ ] Document LLM interactions
