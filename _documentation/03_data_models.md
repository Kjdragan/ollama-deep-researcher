# Data Models and State Management

## Configuration Model
```python
@dataclass
class Configuration:
    max_web_research_loops: int = 3
    local_llm: str = "llama3.2"
```

### Purpose
- Manages configurable parameters
- Supports environment variables
- Integrates with LangGraph configuration

### Usage
- Controls research depth
- Specifies LLM model
- Extensible for future parameters

## State Models

### 1. SummaryState
```python
@dataclass
class SummaryState:
    research_topic: str
    search_query: str
    web_research_results: list
    sources_gathered: list
    research_loop_count: int
    running_summary: str
```

#### Fields
- `research_topic`: Initial research question
- `search_query`: Current search term
- `web_research_results`: List of search results
- `sources_gathered`: Accumulated sources
- `research_loop_count`: Iteration counter
- `running_summary`: Current research state

#### Annotations
- Uses operator.add for list fields
- Supports incremental updates
- Maintains research history

### 2. Input/Output Models
```python
@dataclass
class SummaryStateInput:
    research_topic: str

@dataclass
class SummaryStateOutput:
    running_summary: str
```

#### Purpose
- Define graph interfaces
- Type safety
- Clear data contracts

## State Transitions

### 1. Query Generation
```
Input: research_topic
Update: search_query
```

### 2. Web Research
```
Input: search_query
Update: 
- web_research_results (append)
- sources_gathered (append)
- research_loop_count (increment)
```

### 3. Summarization
```
Input: 
- web_research_results
- running_summary (if exists)
Update: running_summary
```

### 4. Reflection
```
Input: running_summary
Update: search_query
```

### 5. Finalization
```
Input: 
- running_summary
- sources_gathered
Update: running_summary (add sources)
```

## State Management Best Practices

### 1. Immutability
- State updates via new instances
- No direct mutation
- Clear state transitions

### 2. History Tracking
- Accumulates sources
- Maintains research path
- Supports iteration count

### 3. Type Safety
- Dataclass validation
- Clear field purposes
- Structured data flow

### 4. Extension Points
- Annotated fields
- Optional parameters
- Configuration integration
