# Utilities and External Integrations

## Web Search Integration

### Tavily Search
```python
@traceable
def tavily_search(query, include_raw_content=True, max_results=3):
```

#### Parameters
- `query`: Search string
- `include_raw_content`: Full page content flag
- `max_results`: Result limit

#### Features
- Content extraction
- Result limiting
- Tracing support

## Source Processing

### 1. Source Deduplication
```python
def deduplicate_and_format_sources(
    search_response, 
    max_tokens_per_source, 
    include_raw_content=True
)
```

#### Functionality
- URL-based deduplication
- Token limiting
- Content formatting

#### Output Format
```
Sources:

Source [Title]:
===
URL: [URL]
===
Most relevant content: [Content]
===
Full source content: [Raw Content]
```

### 2. Source Formatting
```python
def format_sources(search_results):
```

#### Purpose
- Bullet-point formatting
- URL inclusion
- Title preservation

#### Output Format
```
* [Title] : [URL]
* [Title] : [URL]
```

## Integration Best Practices

### 1. Web Search
- Use appropriate result limits
- Handle missing content
- Implement error handling

### 2. Content Processing
- Token limit enforcement
- Content truncation
- Warning generation

### 3. Source Management
- Deduplication
- Consistent formatting
- Clear attribution

## External Dependencies

### 1. Tavily API
- Search functionality
- Content extraction
- Result formatting

### 2. LangSmith
- Tracing support
- Performance monitoring
- Debug capabilities

## Error Handling

### 1. Input Validation
- Type checking
- Format validation
- Default handling

### 2. Content Processing
- None handling
- Length limits
- Truncation notices

### 3. API Integration
- Connection errors
- Rate limiting
- Response validation

## Performance Considerations

### 1. Result Limiting
- Max results parameter
- Token limiting
- Content truncation

### 2. Deduplication
- URL-based
- Early filtering
- Memory efficient

### 3. Content Processing
- Chunked processing
- Size estimation
- Format optimization
