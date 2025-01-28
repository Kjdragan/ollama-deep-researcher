# PydanticAI Results

Results are the final values returned from running an agent. They are wrapped in `RunResult` and `StreamedRunResult` classes that provide access to additional data like usage statistics and message history.

## Result Types

### Basic Results
```python
from pydantic import BaseModel

class CityLocation(BaseModel):
    city: str
    country: str

agent = Agent('gemini-1.5-flash', result_type=CityLocation)
result = agent.run_sync('Where were the olympics held in 2012?')
print(result.data)  # city='London' country='United Kingdom'
print(result.usage())  # Usage statistics
```

### Union Types
You can use Union types to handle multiple possible result types:

```python
class Box(BaseModel):
    width: int
    height: int
    depth: int
    units: str

agent: Agent[None, Union[Box, str]] = Agent(
    'openai:gpt-4o-mini',
    result_type=Union[Box, str],  # type: ignore
    system_prompt="Extract dimensions or ask for more info"
)
```

Note: Due to Python typing limitations (until PEP-747), unions require type ignores and explicit type hints.

## Result Validation

### Pydantic Validation
Results are validated using Pydantic:
- String results are passed through directly
- Structured results use Pydantic for schema generation and validation
- Union types register multiple tools with the model

### Custom Validators
For complex validation (e.g., async or IO-dependent), use result validators:

```python
@agent.result_validator
async def validate_result(ctx: RunContext[DatabaseConn], result: Response) -> Response:
    if isinstance(result, InvalidRequest):
        return result
    try:
        await ctx.deps.execute(f'EXPLAIN {result.sql_query}')
    except QueryError as e:
        raise ModelRetry(f'Invalid query: {e}') from e
    return result
```

## Streamed Results

### Text Streaming
Stream complete text responses:
```python
async with agent.run_stream('Where does "hello world" come from?') as result:
    async for message in result.stream_text():
        print(message)
```

Stream text deltas (changes):
```python
async with agent.run_stream('Where does "hello world" come from?') as result:
    async for message in result.stream_text(delta=True):
        print(message)
```

### Structured Response Streaming

For structured responses, TypedDict is recommended for better partial validation support:

```python
class UserProfile(TypedDict, total=False):
    name: str
    dob: date
    bio: str

agent = Agent(
    'openai:gpt-4o',
    result_type=UserProfile,
    system_prompt='Extract a user profile from the input'
)

async with agent.run_stream(user_input) as result:
    async for profile in result.stream():
        print(profile)  # Shows progressive updates
```

### Fine-grained Validation Control

For detailed validation control:

```python
async with agent.run_stream(user_input) as result:
    async for message, last in result.stream_structured(debounce_by=0.01):
        try:
            profile = await result.validate_structured_result(
                message,
                allow_partial=not last,
            )
        except ValidationError:
            continue
        print(profile)
```

## Best Practices

1. Use Pydantic models for structured results
2. Consider TypedDict for streamed structured responses
3. Implement custom validators for complex validation logic
4. Handle validation errors gracefully
5. Use appropriate streaming method based on needs:
   - `stream_text()` for complete text updates
   - `stream_text(delta=True)` for text changes
   - `stream()` for structured data
   - `stream_structured()` for fine-grained control
6. Set appropriate debounce values for structured streaming
7. Remember that final result messages may not be included in delta streaming

## Note on Run Completion

Runs end when either:
- A plain text response is received
- The model calls a tool associated with structured result types

Future updates will add limits to prevent indefinite runs.