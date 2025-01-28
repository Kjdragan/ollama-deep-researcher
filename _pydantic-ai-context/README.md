# PydanticAI Documentation Context

This directory contains key documentation and examples from the PydanticAI framework (https://ai.pydantic.dev/).

## Directory Structure

- `introduction.md`: Overview of PydanticAI, its features, and design philosophy
- `agents.md`: Comprehensive guide to PydanticAI Agents, their components, and usage
- `models.md`: Detailed documentation of supported LLM providers and model configuration
- `dependencies.md`: Guide to dependency injection system and testing practices
- `tools.md`: Documentation of function tools, their types, and schema handling
- `results.md`: Guide to result types, validation, and streaming capabilities
- `messages.md`: Documentation of message handling and conversation management
- `testing.md`: Guide to unit testing, evals, and performance measurement
- `monitoring.md`: Guide to debugging and monitoring with Pydantic Logfire
- `multi_agent.md`: Guide to building multi-agent applications and patterns
- `graphs.md`: Guide to graph-based state machines and complex workflows
- `examples.py`: Runnable code examples including:
  - Hello World example using Gemini model
  - Bank Support example demonstrating dependency injection and tools
  - Logfire integration example

## Version Information

Documentation scraped from PydanticAI v0.0.20 (as of 2025-01-23).

## Documentation Sections

### Introduction
- Framework overview
- Key features
- Design philosophy

### Agents
- Core components
- Running agents
- Type safety
- System prompts
- Usage limits
- Model settings
- Conversation management
- Error handling

### Models
- Supported LLM providers:
  - OpenAI
  - Anthropic
  - Gemini (GLA and VertexAI)
  - Ollama
  - Groq
  - Mistral
- OpenAI-compatible models
- Installation requirements
- Configuration guides
- Custom model implementation

### Dependencies
- Dependency injection system
- Sync vs. async dependencies
- Testing with dependencies
- Best practices
- Dependency overriding
- Full examples with system prompts, tools, and validators

### Tools
- Function tool types and registration
- Tool schema generation
- Dynamic function tools
- Tool documentation practices
- RAG vs Function tools comparison
- Best practices for tool implementation
- Examples of different tool types

### Results
- Result types and validation
- Structured responses
- Custom result validators
- Streaming capabilities
  - Text streaming
  - Structured response streaming
  - Fine-grained validation control
- Best practices for result handling

### Messages
- Message access and management
- Conversation context handling
- Message structure and types
- Cross-model message compatibility
- Streaming considerations
- Best practices for message handling
- Advanced usage patterns

### Testing
- Unit testing strategies
  - TestModel usage
  - FunctionModel for complex scenarios
  - Pytest fixtures and patterns
- Evaluation approaches
  - Performance measurement
  - Cross-validation techniques
  - Production metrics
- System prompt testing
- Best practices for testing and evals

### Monitoring
- Debugging and observability
- Pydantic Logfire integration
- Real-time debugging capabilities
- Performance monitoring
- OpenTelemetry support
- Best practices for:
  - Configuration
  - Debugging workflows
  - System monitoring
  - Performance optimization

### Multi-agent Applications
- Agent interaction patterns:
  - Single agent workflows
  - Agent delegation
  - Programmatic hand-off
  - Graph-based control flow
- Dependency management
- State handling
- Usage tracking
- Best practices for:
  - Agent delegation
  - Programmatic control
  - Complex workflows
  - Error handling

### Graphs
- Graph-based state machines
- Core components:
  - GraphRunContext
  - Nodes
  - State management
  - Dependencies
- Custom control flow
- Visualization with Mermaid
- Best practices for:
  - Graph design
  - State management
  - Error handling
  - Documentation

### Examples
The code examples include stub implementations where necessary (like the DatabaseConn class) to make the structure clear while acknowledging that some components would need real implementations in a production environment.

For the complete and up-to-date documentation, visit: https://ai.pydantic.dev/