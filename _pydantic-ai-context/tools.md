# PydanticAI Function Tools

Function tools provide a mechanism for models to retrieve additional information during response generation. They're particularly useful when:
- Context is too large for system prompts
- You need deterministic or reliable behavior
- Logic should be delegated to non-AI components

## Tool Types and Registration

### 1. Context-Aware Tools (`@agent.tool`)
Tools that need access to the agent context:
```python
@agent.tool
def get_player_name(ctx: RunContext[str]) -> str:
    """Get the player's name."""
    return ctx.deps
```

### 2. Context-Free Tools (`@agent.tool_plain`)
Tools that don't need agent context:
```python
@agent.tool_plain
def roll_die() -> str:
    """Roll a six-sided die and return the result."""
    return str(random.randint(1, 6))
```

### 3. Registration via Constructor
Tools can also be registered during agent initialization:
```python
agent = Agent(
    'gemini-1.5-flash',
    deps_type=str,
    tools=[
        Tool(roll_die, takes_ctx=False),
        Tool(get_player_name, takes_ctx=True),
    ],
)
```

## Tool Schema and Documentation

Tools use function signatures and docstrings to generate schemas:

```python
@agent.tool_plain(docstring_format='google', require_parameter_descriptions=True)
def foobar(a: int, b: str, c: dict[str, list[float]]) -> str:
    """Get me foobar.

    Args:
        a: apple pie
        b: banana cake
        c: carrot smoothie
    """
    return f'{a} {b} {c}'
```

Generated schema:
```json
{
    "properties": {
        "a": {"description": "apple pie", "title": "A", "type": "integer"},
        "b": {"description": "banana cake", "title": "B", "type": "string"},
        "c": {
            "additionalProperties": {"items": {"type": "number"}, "type": "array"},
            "description": "carrot smoothie",
            "title": "C",
            "type": "object"
        }
    },
    "required": ["a", "b", "c"],
    "type": "object",
    "additionalProperties": false
}
```

### Single Parameter Tools

When a tool has a single parameter that can be represented as a JSON object, the schema is simplified:

```python
class Foobar(BaseModel):
    """This is a Foobar"""
    x: int
    y: str
    z: float = 3.14

@agent.tool_plain
def foobar(f: Foobar) -> str:
    return str(f)
```

## Dynamic Function Tools

Tools can be dynamically modified or excluded using a `prepare` function:

```python
async def only_if_42(
    ctx: RunContext[int], 
    tool_def: ToolDefinition
) -> Union[ToolDefinition, None]:
    if ctx.deps == 42:
        return tool_def

@agent.tool(prepare=only_if_42)
def hitchhiker(ctx: RunContext[int], answer: str) -> str:
    return f'{ctx.deps} {answer}'
```

### Dynamic Tool Description

Tool descriptions can be modified based on context:

```python
async def prepare_greet(
    ctx: RunContext[Literal['human', 'machine']], 
    tool_def: ToolDefinition
) -> ToolDefinition | None:
    d = f'Name of the {ctx.deps} to greet.'
    tool_def.parameters_json_schema['properties']['name']['description'] = d
    return tool_def

greet_tool = Tool(greet, prepare=prepare_greet)
```

## Best Practices

1. Use descriptive docstrings for clear tool documentation
2. Leverage type hints for accurate schema generation
3. Consider using `prepare` functions for dynamic behavior
4. Keep tools focused and single-purpose
5. Use appropriate tool registration method based on context needs
6. Handle errors gracefully within tools
7. Consider using Pydantic models for complex parameter types

## Note on RAG vs Function Tools

While function tools can be seen as part of RAG (Retrieval-Augmented Generation), they are more general-purpose than traditional RAG implementations:
- RAG typically focuses on vector search
- Function tools can implement any type of information retrieval or computation
- PydanticAI may add dedicated vector search support in the future