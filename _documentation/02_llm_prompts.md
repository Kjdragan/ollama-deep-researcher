# LLM Prompts and Interactions

## Overview
The system uses three specialized prompts for different stages of the research process. Each prompt is carefully designed for a specific task in the research workflow.

## 1. Query Writer
### Purpose
Generates targeted web search queries based on the research topic.

### Prompt Structure
```
Input:
- Research topic

Output Format (JSON):
{
    "query": "search query string",
    "aspect": "aspect being researched",
    "rationale": "reasoning behind query"
}
```

### Key Design Elements
- Focused on generating search-engine optimized queries
- Includes metadata about the search intent
- Structured JSON output for consistency

## 2. Summarizer
### Purpose
Creates and extends research summaries based on web search results.

### Behaviors
1. New Summary Creation:
   - Highlights relevant information
   - Provides concise overviews
   - Emphasizes key findings
   - Maintains coherent flow

2. Summary Extension:
   - Integrates new information seamlessly
   - Avoids repetition
   - Maintains consistent style
   - Ensures smooth transitions

### Critical Requirements
- Direct content focus
- No meta-commentary
- Objective information only
- Consistent technical depth
- No explicit source references in text

## 3. Reflection Engine
### Purpose
Analyzes current knowledge and identifies areas for deeper research.

### Prompt Structure
```
Input:
- Research topic
- Current summary

Output Format (JSON):
{
    "knowledge_gap": "identified gap description",
    "follow_up_query": "next search query"
}
```

### Key Features
- Expert research assistant persona
- Focus on technical details
- Self-contained follow-up queries
- Structured gap analysis

## LLM Configuration
- Uses Ollama for local LLM hosting
- JSON mode for structured outputs
- Temperature = 0 for consistency
- Model specified in configuration

## Best Practices
1. Query Generation
   - Keep queries focused and specific
   - Include necessary context
   - Optimize for search engine syntax

2. Summarization
   - Maintain consistent voice
   - Progressive information building
   - Clean, professional style

3. Reflection
   - Technical depth in analysis
   - Contextual follow-up queries
   - Clear gap identification
