# Prompt Templates Analysis

## Query Writer Prompt

### Template Structure
```python
query_writer_instructions = """Your goal is to generate targeted web search query.

The query will gather information related to a specific topic.

Topic:
{research_topic}

Return your query as a JSON object:
{
    "query": "string",
    "aspect": "string",
    "rationale": "string"
}
"""
```

### Implementation Details
1. **Format Parameters**
   - research_topic: Main research subject
   - Dynamic insertion via string formatting

2. **Output Structure**
   - JSON format enforced
   - Three key components:
     * query: Search string
     * aspect: Research focus
     * rationale: Query justification

3. **Usage Pattern**
   ```python
   llm_json_mode = ChatOllama(
       model=configurable.local_llm,
       temperature=0,
       format="json"
   )
   ```

## Summarizer Prompt

### Template Structure
```python
summarizer_instructions = """Your goal is to generate a high-quality summary of the web search results.

When EXTENDING an existing summary:
1. Seamlessly integrate new information
2. Maintain consistency
3. Only add non-redundant information
4. Ensure smooth transitions

When creating a NEW summary:
1. Highlight relevant information
2. Provide concise overview
3. Emphasize significant findings
4. Ensure coherent flow

CRITICAL REQUIREMENTS:
- Start IMMEDIATELY with content
- NO meta-commentary
- Focus on factual information
- Maintain technical depth
- Avoid redundancy
"""
```

### Implementation Details
1. **Dual Mode Support**
   - New summary creation
   - Summary extension

2. **Content Guidelines**
   - Direct content focus
   - Professional style
   - Technical accuracy

3. **Usage Pattern**
   ```python
   llm = ChatOllama(
       model=configurable.local_llm,
       temperature=0
   )
   ```

## Reflection Prompt

### Template Structure
```python
reflection_instructions = """You are an expert research assistant analyzing a summary about {research_topic}.

Your tasks:
1. Identify knowledge gaps
2. Generate follow-up question
3. Focus on technical details

Return your analysis as a JSON object:
{
    "knowledge_gap": "string",
    "follow_up_query": "string"
}
"""
```

### Implementation Details
1. **Format Parameters**
   - research_topic: Context for analysis
   - Dynamic topic insertion

2. **Output Structure**
   - JSON format
   - Two key components:
     * knowledge_gap: Identified gap
     * follow_up_query: Next search

3. **Usage Pattern**
   ```python
   llm_json_mode = ChatOllama(
       model=configurable.local_llm,
       temperature=0,
       format="json"
   )
   ```

## Prompt Design Patterns

### 1. Clarity
- Clear instructions
- Specific requirements
- Structured output

### 2. Consistency
- JSON formatting
- Temperature=0
- Deterministic outputs

### 3. Context Management
- Topic preservation
- State awareness
- Progressive refinement

## Implementation Best Practices

### 1. Output Format
- JSON structure
- Clear schema
- Validation support

### 2. Error Handling
- Format validation
- Content cleaning
- Tag removal

### 3. Model Configuration
- Zero temperature
- Format specification
- Model consistency

## Extension Points

### 1. New Prompts
- Follow template pattern
- Maintain consistency
- Clear instructions

### 2. Output Formats
- JSON schema updates
- New fields
- Validation rules

### 3. Context Management
- Additional parameters
- State references
- Dynamic content
