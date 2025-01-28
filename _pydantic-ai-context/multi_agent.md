# PydanticAI Multi-agent Applications

PydanticAI supports four levels of complexity for building multi-agent applications:
1. Single agent workflows
2. Agent delegation
3. Programmatic agent hand-off
4. Graph-based control flow

## Agent Delegation

Agent delegation allows one agent to delegate work to another agent through tools, then regain control after completion.

### Key Points
- Agents are stateless and designed to be global
- No need to include agent in dependencies
- Pass `ctx.usage` to track total usage
- Can use different models for different agents

Example:
```python
from pydantic_ai import Agent, RunContext
from pydantic_ai.usage import UsageLimits

joke_selection_agent = Agent(
    'openai:gpt-4o',
    system_prompt='Use the `joke_factory` to generate some jokes, then choose the best.'
)
joke_generation_agent = Agent('gemini-1.5-flash', result_type=list[str])

@joke_selection_agent.tool
async def joke_factory(ctx: RunContext[None], count: int) -> list[str]:
    r = await joke_generation_agent.run(
        f'Please generate {count} jokes.',
        usage=ctx.usage,
    )
    return r.data
```

### Dependencies in Delegation

Dependencies should follow these patterns:
1. Delegate agent uses same or subset of parent's dependencies
2. Initialize new dependencies within tool call (less efficient)

Example with shared dependencies:
```python
@dataclass
class ClientAndKey:
    http_client: httpx.AsyncClient
    api_key: str

joke_selection_agent = Agent(
    'openai:gpt-4o',
    deps_type=ClientAndKey,
    system_prompt='Use the `joke_factory` tool...'
)

@joke_selection_agent.tool
async def joke_factory(ctx: RunContext[ClientAndKey], count: int) -> list[str]:
    r = await joke_generation_agent.run(
        f'Please generate {count} jokes.',
        deps=ctx.deps,
        usage=ctx.usage,
    )
    return r.data
```

## Programmatic Agent Hand-off

This pattern involves multiple agents called in succession, with application code or human interaction determining the sequence.

Key characteristics:
- Agents can use different dependencies
- Control flow managed by application code
- Supports human-in-the-loop interactions
- Flexible state management

Example flight booking system:
```python
class FlightDetails(BaseModel):
    flight_number: str

class SeatPreference(BaseModel):
    row: int = Field(ge=1, le=30)
    seat: Literal['A', 'B', 'C', 'D', 'E', 'F']

flight_search_agent = Agent[None, Union[FlightDetails, Failed]](
    'openai:gpt-4o',
    result_type=Union[FlightDetails, Failed],
    system_prompt='Use the "flight_search" tool...'
)

seat_preference_agent = Agent[None, Union[SeatPreference, Failed]](
    'openai:gpt-4o',
    result_type=Union[SeatPreference, Failed],
    system_prompt='Extract the user\'s seat preference...'
)

async def main():
    usage: Usage = Usage()
    
    # First agent: Find flight
    flight_details = await find_flight(usage)
    if flight_details:
        # Second agent: Get seat preference
        seat_preference = await find_seat(usage)
```

## Best Practices

1. Agent Delegation
   - Pass usage context to track total usage
   - Consider dependency sharing for efficiency
   - Use appropriate model for each agent
   - Handle errors at each delegation level

2. Programmatic Hand-off
   - Clear state management between agents
   - Proper error handling and retries
   - User interaction management
   - Usage tracking across agents

3. General Guidelines
   - Choose appropriate complexity level
   - Document agent interactions
   - Monitor performance and usage
   - Handle errors gracefully
   - Consider user experience in interactive systems

## Graph-based Control Flow

For complex applications, PydanticAI supports graph-based state machines to control agent execution. See the graph documentation for detailed implementation.

## Note on Complexity

Choose the appropriate level of complexity based on your needs:
- Single agent for simple tasks
- Agent delegation for modular functionality
- Programmatic hand-off for interactive flows
- Graph-based for complex state management

The patterns can be combined as needed within a single application.