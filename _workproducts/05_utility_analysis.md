# Utility Functions Analysis

## Web Search Integration

### Tavily Search Implementation
```python
@traceable
def tavily_search(query, include_raw_content=True, max_results=3):
    tavily_client = TavilyClient()
    return tavily_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content
    )
```

### Key Features
1. **Tracing Support**
   - @traceable decorator
   - Performance monitoring
   - Debugging support

2. **Configuration Options**
   - Raw content inclusion
   - Result limiting
   - Client management

3. **Return Structure**
   ```python
   {
       'results': [
           {
               'title': str,
               'url': str,
               'content': str,
               'raw_content': str
           }
       ]
   }
   ```

## Source Processing

### Deduplication Function
```python
def deduplicate_and_format_sources(
    search_response,
    max_tokens_per_source,
    include_raw_content=True
):
    # Input handling
    sources_list = _extract_sources(search_response)
    
    # Deduplication
    unique_sources = {
        source['url']: source
        for source in sources_list
    }
    
    # Formatting
    return _format_sources(
        unique_sources,
        max_tokens_per_source,
        include_raw_content
    )
```

### Implementation Details
1. **Input Processing**
   - Handles dict/list inputs
   - Extracts source lists
   - Validates structure

2. **Deduplication Logic**
   - URL-based uniqueness
   - Dictionary mapping
   - Order preservation

3. **Content Formatting**
   - Token limiting
   - Content truncation
   - Source attribution

## Source Formatting

### Format Function
```python
def format_sources(search_results):
    return '\n'.join(
        f"* {source['title']} : {source['url']}"
        for source in search_results['results']
    )
```

### Features
1. **Output Structure**
   - Bullet-point format
   - Title inclusion
   - URL reference

2. **Implementation**
   - List comprehension
   - String joining
   - Clean formatting

## Error Handling

### 1. Input Validation
```python
if not isinstance(search_response, (dict, list)):
    raise ValueError(
        "Input must be dict or list"
    )
```

### 2. Content Processing
```python
raw_content = source.get('raw_content', '')
if raw_content is None:
    raw_content = ''
    print(f"Warning: No raw_content for {source['url']}")
```

### 3. Token Management
```python
if len(raw_content) > char_limit:
    raw_content = raw_content[:char_limit] + "... [truncated]"
```

## Performance Optimizations

### 1. Memory Management
- Early deduplication
- Content truncation
- Efficient string handling

### 2. Processing Efficiency
- List comprehensions
- Dictionary lookups
- Minimal iterations

### 3. Resource Usage
- Result limiting
- Content size control
- Warning generation

## Extension Points

### 1. Search Integration
- New search providers
- Additional parameters
- Result formatting

### 2. Source Processing
- Custom deduplication
- Format variations
- Content filtering

### 3. Error Handling
- Custom validators
- Warning systems
- Recovery strategies

## Implementation Best Practices

### 1. Code Organization
- Clear function purposes
- Single responsibility
- Type hints

### 2. Error Management
- Explicit validation
- Clear messages
- Recovery paths

### 3. Performance
- Early optimization
- Resource control
- Clear limitations
