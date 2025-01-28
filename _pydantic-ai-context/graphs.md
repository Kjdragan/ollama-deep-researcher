# PydanticAI Graphs

PydanticAI provides powerful graph-based state machines for complex workflows through the `pydantic-graph` library.

## Overview

> "If PydanticAI agents are a hammer, and multi-agent workflows are a sledgehammer, then graphs are a nail gun."

Consider simpler approaches (single agent, agent delegation, programmatic hand-off) before using graphs. Graphs add complexity but provide powerful control flow for complex scenarios.

## Installation

```bash
# Using pip
pip install pydantic-graph

# Using uv
uv add pydantic-graph
```

## Core Components

### 1. GraphRunContext
- Holds graph state and dependencies
- Generic in state type (StateT)
- Similar to PydanticAI's RunContext

### 2. End
- Signals graph run completion
- Generic in return type (RunEndT)
- Used to terminate graph execution

### 3. Nodes
Nodes are dataclasses that inherit from BaseNode:
```python
@dataclass
class MyNode(BaseNode[StateT, DepsT, RunEndT]):
    foo: int

    async def run(
        self,
        ctx: GraphRunContext[StateT]
    ) -> AnotherNode | End[RunEndT]:
        if some_condition:
            return End(result)
        return AnotherNode()
```

Generic parameters:
- `StateT`: Graph state type
- `DepsT`: Dependencies type
- `RunEndT`: Return type when ending

### 4. Graph
Container for node execution:
```python
graph = Graph(nodes=[NodeA, NodeB, NodeC])
result, history = graph.run_sync(NodeA(foo=1))
```

## State Management

Graphs can maintain state across nodes:

```python
@dataclass
class MachineState:
    balance: float = 0.0
    product: str | None = None

@dataclass
class InsertCoin(BaseNode[MachineState]):
    async def run(self, ctx: GraphRunContext[MachineState]) -> NextNode:
        ctx.state.balance += amount
        return NextNode()
```

## Dependency Injection

Support for dependency injection similar to PydanticAI:

```python
@dataclass
class GraphDeps:
    executor: ProcessPoolExecutor

@dataclass
class ComputeNode(BaseNode[None, GraphDeps]):
    async def run(self, ctx: GraphRunContext) -> NextNode:
        result = await ctx.deps.executor.submit(heavy_computation)
        return NextNode(result)
```

## Custom Control Flow

### Step-by-step Execution
For scenarios requiring external input or long-running operations:

```python
async def run_with_input():
    state = QuestionState()
    node = StartNode()
    history = []
    
    while True:
        node = await graph.next(node, history, state=state)
        if isinstance(node, UserInputNode):
            node.input = await get_user_input()
        elif isinstance(node, End):
            return node.data
```

## Visualization

### Mermaid Diagrams
Generate visual representations of graphs:

```python
# Basic diagram
graph.mermaid_code(start_node=StartNode)

# With customizations
graph.mermaid_code(
    start_node=StartNode,
    direction='LR',  # Left to Right flow
    highlighted_nodes=[CurrentNode]
)

# Save as image
graph.mermaid_save('graph.png', start_node=StartNode)
```

### Edge Labels and Notes
Add context to diagrams:
```python
@dataclass
class Node(BaseNode):
    """Node documentation becomes a note."""
    docstring_notes = True
    
    async def run(
        self,
        ctx: GraphRunContext
    ) -> Annotated[NextNode, Edge(label="transition label")]:
        return NextNode()
```

## Best Practices

1. Graph Usage
   - Consider simpler approaches first
   - Use for complex, stateful workflows
   - Break large graphs into manageable components

2. State Management
   - Keep state minimal and focused
   - Use dataclasses or Pydantic models
   - Consider persistence needs

3. Dependencies
   - Share resources efficiently
   - Handle cleanup properly
   - Use dependency injection for testing

4. Visualization
   - Document graph structure
   - Use meaningful edge labels
   - Add notes for complex nodes
   - Choose appropriate diagram direction

5. Error Handling
   - Handle node failures gracefully
   - Implement proper cleanup
   - Consider retry strategies

## Note on Early Beta

Graph support is in early beta (introduced in v0.0.19):
- API may change
- Documentation is evolving
- Implementation is being refined

Consider stability requirements when adopting graph functionality.