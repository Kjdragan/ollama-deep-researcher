# PydanticAI Models

PydanticAI is model-agnostic and supports multiple LLM providers out of the box.

## Supported Models

### OpenAI
- Installation: `pip install 'pydantic-ai-slim[openai]'`
- Configuration: 
  - Get API key from platform.openai.com
  - Set via `OPENAI_API_KEY` environment variable or pass directly
  - Supports Azure OpenAI via custom client
```python
from pydantic_ai import Agent
agent = Agent('openai:gpt-4o')
```

### Anthropic
- Installation: `pip install 'pydantic-ai-slim[anthropic]'`
- Configuration:
  - Get API key from console.anthropic.com/settings/keys
  - Set via `ANTHROPIC_API_KEY` environment variable or pass directly
```python
from pydantic_ai import Agent
agent = Agent('claude-3-5-sonnet-latest')
```

### Gemini
Two APIs available:
1. Generative Language API (for prototyping)
   - No extra dependencies required
   - Get API key from aistudio.google.com
   - Set via `GEMINI_API_KEY` environment variable
```python
from pydantic_ai import Agent
agent = Agent('google-gla:gemini-1.5-flash')
```

2. VertexAI API (for production)
   - Installation: `pip install 'pydantic-ai-slim[vertexai]'`
   - Advantages:
     - More reliable with lower latency
     - Supports provisioned throughput
     - Native GCP integration
     - Region selection available
```python
from pydantic_ai.models.vertexai import VertexAIModel
model = VertexAIModel('gemini-1.5-flash', region='asia-east1')
```

### Ollama
- Installation: `pip install 'pydantic-ai-slim[openai]'`
- Requires:
  - Ollama client installation
  - Running Ollama server
  - Model download from Ollama model library

### Groq
- Installation: `pip install 'pydantic-ai-slim[groq]'`
- Configuration:
  - Get API key from console.groq.com/keys
  - Set via `GROQ_API_KEY` environment variable or pass directly
```python
from pydantic_ai import Agent
agent = Agent('groq:llama-3.3-70b-versatile')
```

### Mistral
- Installation: `pip install 'pydantic-ai-slim[mistral]'`
- Configuration:
  - Get API key from console.mistral.ai/api-keys/
  - Set via `MISTRAL_API_KEY` environment variable or pass directly
```python
from pydantic_ai import Agent
agent = Agent('mistral:mistral-large-latest')
```

## OpenAI-Compatible Models

Many models support the OpenAI API format and can be used with OpenAIModel:

### OpenRouter
```python
from pydantic_ai.models.openai import OpenAIModel
model = OpenAIModel(
    'anthropic/claude-3.5-sonnet',
    base_url='https://openrouter.ai/api/v1',
    api_key='your-openrouter-api-key',
)
```

### Grok (xAI)
```python
from pydantic_ai.models.openai import OpenAIModel
model = OpenAIModel(
    'grok-2-1212',
    base_url='https://api.x.ai/v1',
    api_key='your-xai-api-key',
)
```

### DeepSeek
```python
from pydantic_ai.models.openai import OpenAIModel
model = OpenAIModel(
    'deepseek-chat',
    base_url='https://api.deepseek.com',
    api_key='your-deepseek-api-key',
)
```

## Implementing Custom Models

To add support for new models:
1. Subclass the `Model` abstract base class
2. Implement required abstract base classes:
   - `AgentModel`
   - `StreamedResponse`
3. Review existing implementations (e.g., OpenAIModel) as reference

For contribution guidelines on adding new models to PydanticAI, see the contributing documentation.