# PydanticAI Introduction

PydanticAI is a Python agent framework designed to make it less painful to build production grade applications with Generative AI.

FastAPI revolutionized web development by offering an innovative and ergonomic design, built on the foundation of Pydantic. Similarly, virtually every agent framework and LLM library in Python uses Pydantic, yet when we began to use LLMs in Pydantic Logfire, we couldn't find anything that gave us the same feeling.

We built PydanticAI with one simple aim: to bring that FastAPI feeling to GenAI app development.

## Key Features

- **Built by the Pydantic Team**: Built by the team behind Pydantic (the validation layer of the OpenAI SDK, the Anthropic SDK, LangChain, LlamaIndex, AutoGPT, Transformers, CrewAI, Instructor and many more).
- **Model-agnostic**: Supports OpenAI, Anthropic, Gemini, Ollama, Groq, and Mistral, and there is a simple interface to implement support for other models.
- **Pydantic Logfire Integration**: Seamlessly integrates with Pydantic Logfire for real-time debugging, performance monitoring, and behavior tracking of your LLM-powered applications.
- **Type-safe**: Designed to make type checking as powerful and informative as possible for you.
- **Python-centric Design**: Leverages Python's familiar control flow and agent composition to build your AI-driven projects.
- **Structured Responses**: Harnesses the power of Pydantic to validate and structure model outputs.
- **Dependency Injection System**: Offers an optional dependency injection system to provide data and services.
- **Streamed Responses**: Provides the ability to stream LLM outputs continuously.
- **Graph Support**: Pydantic Graph provides a powerful way to define graphs using typing hints.

> Note: PydanticAI is in early beta, the API is still subject to change and there's a lot more to do.