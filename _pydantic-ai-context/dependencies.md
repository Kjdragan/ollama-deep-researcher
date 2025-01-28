# PydanticAI Dependencies

PydanticAI uses a dependency injection system to provide data and services to your agent's system prompts, tools, and result validators. The system follows Python best practices to ensure type safety, testability, and production readiness.

## Core Concepts

### Defining Dependencies

Dependencies can be any Python type:
- Simple objects (e.g., HTTP connection)
- Dataclasses for multiple objects
- Custom classes with methods

Example:
```python
from dataclasses import dataclass
import httpx

@dataclass
class MyDeps:
    api_key: str
    http_client: httpx.AsyncClient

agent = Agent(
    'openai:gpt-4o',
    deps_type=MyDeps,
)
```

### Accessing Dependencies

Dependencies are accessed through the `RunContext` type in:
- System prompt functions
- Tools
- Result validators

Example:
```python
@agent.system_prompt
async def get_system_prompt(ctx: RunContext[MyDeps]) -> str:
    response = await ctx.deps.http_client.get(
        'https://example.com',
        headers={'Authorization': f'Bearer {ctx.deps.api_key}'},
    )
    response.raise_for_status()
    return f'Prompt: {response.text}'
```

## Asynchronous vs. Synchronous Dependencies

### Key Points
- All agent runs occur in async context
- Both sync and async dependencies are supported
- Sync functions run in thread pool via `run_in_executor`
- Async is preferred for IO operations but not required

### Sync Example:
```python
@dataclass
class MyDeps:
    api_key: str
    http_client: httpx.Client  # Sync client

@agent.system_prompt
def get_system_prompt(ctx: RunContext[MyDeps]) -> str:
    response = ctx.deps.http_client.get(
        'https://example.com',
        headers={'Authorization': f'Bearer {ctx.deps.api_key}'}
    )
    return f'Prompt: {response.text}'
```

## Testing with Dependencies

### Overriding Dependencies

Dependencies can be overridden for testing using the `override` method:

```python
class TestMyDeps(MyDeps):
    async def system_prompt_factory(self) -> str:
        return 'test prompt'

async def test_application_code():
    test_deps = TestMyDeps('test_key', None)
    with joke_agent.override(deps=test_deps):
        result = await application_code('Tell me a joke.')
    assert result.startswith('Did you hear about the toothpaste scandal?')
```

## Best Practices

1. Use dataclasses for organizing multiple dependencies
2. Prefer async dependencies for IO operations
3. Create interfaces for dependencies to enable easy mocking
4. Use dependency overriding for testing
5. Consider creating factory methods in dependency classes for complex setup
6. Handle dependency cleanup properly (e.g., using async context managers)

## Full Example

Here's a complete example showing dependencies used in system prompts, tools, and result validators:

```python
@dataclass
class MyDeps:
    api_key: str
    http_client: httpx.AsyncClient

agent = Agent('openai:gpt-4o', deps_type=MyDeps)

@agent.system_prompt
async def get_system_prompt(ctx: RunContext[MyDeps]) -> str:
    response = await ctx.deps.http_client.get('https://example.com')
    return f'Prompt: {response.text}'

@agent.tool
async def get_joke_material(ctx: RunContext[MyDeps], subject: str) -> str:
    response = await ctx.deps.http_client.get(
        'https://example.com#jokes',
        params={'subject': subject},
        headers={'Authorization': f'Bearer {ctx.deps.api_key}'},
    )
    return response.text

@agent.result_validator
async def validate_result(ctx: RunContext[MyDeps], final_response: str) -> str:
    response = await ctx.deps.http_client.post(
        'https://example.com#validate',
        headers={'Authorization': f'Bearer {ctx.deps.api_key}'},
        params={'query': final_response},
    )
    if response.status_code == 400:
        raise ModelRetry(f'invalid response: {response.text}')
    return final_response
```

This example demonstrates:
- Dependency definition using dataclass
- Async HTTP client dependency
- Dependencies used in system prompts, tools, and validators
- Error handling and validation
- API key management