# PydanticAI Agents

Agents are PydanticAI's primary interface for interacting with LLMs. They can be used individually to control an entire application/component or work together in more complex workflows.

## Core Components

| Component | Description |
|-----------|-------------|
| System prompt(s) | A set of instructions for the LLM written by the developer |
| Function tool(s) | Functions that the LLM may call to get information while generating a response |
| Structured result type | The structured datatype the LLM must return at the end of a run |
| Dependency type constraint | System prompt functions, tools, and result validators may use dependencies |
| LLM model | Optional default LLM model associated with the agent |
| Model Settings | Optional default model settings to help fine tune requests |

## Running Agents

There are three ways to run an agent:

1. `agent.run()` - async coroutine returning a RunResult
2. `agent.run_sync()` - synchronous function returning a RunResult
3. `agent.run_stream()` - async coroutine returning a StreamedRunResult for streaming responses

## Key Features

### Type Safety
- Agents are generic in dependency and result types
- Works well with static type checkers (mypy, pyright)
- Type hints used for runtime validation through Pydantic

### System Prompts
Two categories:
1. Static system prompts: Defined via `system_prompt` parameter
2. Dynamic system prompts: Defined via `@agent.system_prompt` decorated functions

### Usage Limits
Control token usage and request limits:
```python
from pydantic_ai.usage import UsageLimits

agent.run_sync(
    'query',
    usage_limits=UsageLimits(response_tokens_limit=10)
)
```

### Model Settings
Fine-tune model behavior:
```python
agent.run_sync(
    'query',
    model_settings={'temperature': 0.0}
)
```

### Conversation Management
- Single run can handle multiple message exchanges
- Conversations can span multiple runs using message history
- Previous messages can be passed to continue conversations

### Error Handling and Retries
- Validation errors can trigger model retries
- `ModelRetry` can be raised from tools/validators
- `UnexpectedModelBehavior` raised for model errors
- `capture_run_messages()` helps diagnose issues

## Best Practices

1. Agents should be instantiated once and reused (like FastAPI apps)
2. Use type hints for better IDE support and validation
3. Consider using both static and dynamic system prompts when needed
4. Implement proper error handling with retries
5. Use usage limits to prevent excessive token usage or infinite loops
6. Leverage model settings for fine-tuning responses

## Example: Roulette Wheel Agent

```python
from pydantic_ai import Agent, RunContext

roulette_agent = Agent(  
    'openai:gpt-4o',
    deps_type=int,
    result_type=bool,
    system_prompt=(
        'Use the `roulette_wheel` function to see if the '
        'customer has won based on the number they provide.'
    ),
)

@roulette_agent.tool
async def roulette_wheel(ctx: RunContext[int], square: int) -> str:  
    """check if the square is a winner"""
    return 'winner' if square == ctx.deps else 'loser'

# Usage
success_number = 18  
result = roulette_agent.run_sync('Put my money on square eighteen', deps=success_number)
print(result.data)  # True

result = roulette_agent.run_sync('I bet five is the winner', deps=success_number)
print(result.data)  # False