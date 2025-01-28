# Chat App with FastAPI Example

A simple chat application demonstrating PydanticAI integration with FastAPI.

## Features

- Chat history reuse
- Message serialization
- Response streaming
- SQLite message storage
- Real-time UI updates

## Components

- `chat_app.py`: FastAPI backend with PydanticAI integration
- `chat_app.html`: Frontend HTML interface
- `chat_app.ts`: TypeScript for UI interaction

## Running the Example

With dependencies installed and environment variables set:

```bash
# Using pip
python -m pydantic_ai_examples.chat_app

# Using uv
uv run -m pydantic_ai_examples.chat_app
```

Then open the app at localhost:8000.

## Implementation Details

### Backend (`chat_app.py`)
- Uses FastAPI for HTTP server
- Integrates PydanticAI for chat functionality
- Implements SQLite storage for message history
- Handles streaming responses

### Frontend (`chat_app.html`, `chat_app.ts`)
- Simple Bootstrap-based UI
- Real-time message updates
- Markdown rendering
- Loading indicators
- Error handling

## Key Features Demonstrated

1. Message History
   - Persistent storage in SQLite
   - Context preservation between requests
   - Message serialization

2. Streaming
   - Real-time response updates
   - Efficient message handling
   - Progress indication

3. Error Handling
   - Frontend error display
   - Backend error management
   - Type safety

4. UI/UX
   - Clean, responsive design
   - Loading states
   - Smooth scrolling
   - Message formatting