# Question Graph Example

A graph-based implementation of a question-and-answer system using PydanticAI and pydantic-graph.

## Features

- Graph-based state machine
- Multiple execution modes (continuous, CLI)
- History persistence
- Question generation and evaluation
- Mermaid diagram generation

## Components

- Question generation using OpenAI GPT-4
- Answer evaluation
- State management
- History tracking
- Graph visualization

## Running the Example

With dependencies installed and environment variables set:

```bash
# Using pip
python -m pydantic_ai_examples.question_graph

# Using uv
uv run -m pydantic_ai_examples.question_graph
```

### Running Modes

1. Continuous Mode:
```bash
uv run -m pydantic_ai_examples.question_graph continuous
```

2. CLI Mode:
```bash
uv run -m pydantic_ai_examples.question_graph cli [answer]
```

3. Generate Mermaid Diagram:
```bash
uv run -m pydantic_ai_examples.question_graph mermaid
```

## Implementation Details

### Graph Nodes
- `Ask`: Generates questions using GPT-4
- `Answer`: Handles user responses
- `Evaluate`: Assesses answer correctness
- `Congratulate`: Handles correct answers
- `Reprimand`: Handles incorrect answers

### State Management
- Question tracking
- Message history for agents
- Persistent history storage

### Key Features Demonstrated

1. Graph Structure
   - Node definitions
   - Edge relationships
   - State management
   - Flow control

2. Agent Integration
   - Question generation
   - Answer evaluation
   - Message history

3. Execution Modes
   - Interactive continuous mode
   - CLI with history
   - Diagram generation

4. Error Handling
   - State assertions
   - Input validation
   - History management