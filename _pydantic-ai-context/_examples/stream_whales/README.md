# Stream Whales Example

A demonstration of streaming structured responses with PydanticAI, showing real-time validation and display of whale information.

## Features

- Structured response streaming
- Real-time data validation
- Dynamic table updates
- Rich CLI interface

## Components

- Whale data model with validation
- Streaming response handling
- Rich table visualization
- Error handling for partial responses

## Running the Example

With dependencies installed and environment variables set:

```bash
# Using pip
python -m pydantic_ai_examples.stream_whales

# Using uv
uv run -m pydantic_ai_examples.stream_whales
```

## Implementation Details

### Data Model
```python
class Whale(TypedDict):
    name: str
    length: Annotated[float, Field(description='Average length in meters')]
    weight: NotRequired[Annotated[float, Field(description='Weight in kg')]]
    ocean: NotRequired[str]
    description: NotRequired[str]
```

### Key Features Demonstrated

1. Structured Streaming
   - Real-time response processing
   - Partial data validation
   - Progressive UI updates

2. Data Validation
   - Type checking
   - Required vs optional fields
   - Field constraints
   - Error handling

3. Rich UI
   - Live table updates
   - Formatted display
   - Progress indication
   - Error presentation

4. Best Practices
   - Type safety
   - Error handling
   - User feedback
   - Clean data presentation

## Output Example

The example generates a dynamic table showing:
- Whale species name
- Average length
- Average weight
- Ocean habitat
- Brief description

Data is displayed progressively as it's received and validated from the model.