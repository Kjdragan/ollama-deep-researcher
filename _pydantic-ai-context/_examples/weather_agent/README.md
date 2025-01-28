# Weather Agent Example

A PydanticAI agent that provides weather information for multiple locations using external APIs.

## Features

- Multiple tool integration
- Agent dependencies
- Streaming text responses
- Optional Gradio UI
- API integration with fallbacks

## Components

- Weather agent with geocoding and weather tools
- Dependency injection for API clients
- Gradio-based chat interface
- Error handling and retries

## Running the Example

### API Keys (Optional)
The example can run with dummy data, but for real weather information you'll need:
- Weather API key from tomorrow.io (set as `WEATHER_API_KEY`)
- Geocoding API key from geocode.maps.co (set as `GEO_API_KEY`)

### Basic Agent
```bash
# Using pip
python -m pydantic_ai_examples.weather_agent

# Using uv
uv run -m pydantic_ai_examples.weather_agent
```

### Gradio UI
```bash
# Install Gradio
pip install gradio>=5.9.0

# Run the UI
python -m pydantic_ai_examples.weather_agent_gradio
```

## Implementation Details

### Agent Tools
1. `get_lat_lng`
   - Geocoding location to coordinates
   - Fallback to dummy data
   - Error handling with retries

2. `get_weather`
   - Weather data retrieval
   - Temperature and conditions
   - Comprehensive weather codes
   - Metric unit support

### Key Features Demonstrated

1. Tool Integration
   - Multiple tool coordination
   - API integration
   - Error handling
   - Fallback responses

2. Dependencies
   - HTTP client management
   - API key handling
   - Clean dependency injection

3. User Interface
   - Basic CLI interface
   - Rich Gradio chat UI
   - Multi-turn conversations
   - Real-time responses

4. Best Practices
   - Environment configuration
   - Error handling
   - API retries
   - Clean code structure

## Weather Codes

The agent supports a comprehensive set of weather conditions:
- Clear/Sunny (1000)
- Cloudy conditions (1001-1102)
- Fog (2000-2100)
- Rain (4000-4201)
- Snow (5000-5101)
- Freezing conditions (6000-6201)
- Ice pellets (7000-7102)
- Thunderstorm (8000)