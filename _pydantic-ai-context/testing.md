# PydanticAI Testing and Evals

PydanticAI supports two distinct types of testing:
1. Unit tests - Testing application code behavior
2. Evals - Testing LLM response quality

## Unit Testing

### Best Practices
- Use pytest as test harness
- Use inline-snapshot for long assertions
- Use dirty-equals for comparing data structures
- Use TestModel or FunctionModel to avoid real LLM calls
- Use Agent.override to replace models in application logic
- Set `ALLOW_MODEL_REQUESTS=False` to prevent accidental real model calls

### Testing with TestModel

TestModel provides a simple way to test application code:
```python
from pydantic_ai import models, capture_run_messages
from pydantic_ai.models.test import TestModel

# Prevent real model requests
models.ALLOW_MODEL_REQUESTS = False

async def test_forecast():
    conn = DatabaseConn()
    with capture_run_messages() as messages:
        with weather_agent.override(model=TestModel()):
            await run_weather_forecast([("What's the weather?", 1)], conn)
            
    # Verify results and message flow
    forecast = await conn.get_forecast(1)
    assert forecast == '{"weather_forecast":"Sunny with a chance of rain"}'
```

Note: TestModel generates valid but not necessarily meaningful data based on tool schemas.

### Testing with FunctionModel

For more control over tool behavior:
```python
def call_weather_forecast(
    messages: list[ModelMessage],
    info: AgentInfo
) -> ModelResponse:
    if len(messages) == 1:
        # First call - extract date and return tool call
        user_prompt = messages[0].parts[-1]
        date_match = re.search(r'\d{4}-\d{2}-\d{2}', user_prompt.content)
        args = {'location': 'London', 'forecast_date': date_match.group()}
        return ModelResponse(parts=[ToolCallPart('weather_forecast', args)])
    else:
        # Second call - return forecast
        msg = messages[-1].parts[0]
        return ModelResponse(parts=[TextPart(f'The forecast is: {msg.content}')])

async def test_forecast_future():
    with weather_agent.override(model=FunctionModel(call_weather_forecast)):
        await run_weather_forecast(...)
```

### Using Pytest Fixtures

For reusable model overrides:
```python
@pytest.fixture
def override_weather_agent():
    with weather_agent.override(model=TestModel()):
        yield

async def test_forecast(override_weather_agent: None):
    # Test code here
```

## Evals

Evals are used to evaluate model performance for specific applications. Unlike unit tests, evals:
- Are more like benchmarks than pass/fail tests
- Focus on performance changes over time
- Can be slow and expensive to run
- Usually not run in CI for every commit

### Performance Measurement Strategies

1. End-to-end Tests
   - Test final results directly (e.g., SQL query validity)
   - Quick feedback loop
   - Clear success criteria

2. Synthetic Tests
   - Unit test style checks
   - Simple but effective
   - Easy to diagnose failures

3. LLM-based Evaluation
   - Using models to evaluate other models
   - Useful in certain contexts
   - Consider limitations carefully

4. Production Metrics
   - Measure real-world performance
   - Create quantitative metrics
   - Track changes over time
   - Use tools like logfire for analysis

### Example: SQL Generation Eval

Using cross-validation to evaluate SQL generation:
```python
async def evaluate_sql_generation():
    # Load test cases
    examples = load_examples()
    fold_size = len(examples) // 5
    folds = create_folds(examples, fold_size)
    scores = []

    for i, test_fold in enumerate(folds):
        # Use other folds for training
        train_folds = [f for j, f in enumerate(folds) if j != i]
        system_prompt = SqlSystemPrompt(examples=train_folds)

        with sql_agent.override(deps=system_prompt):
            fold_score = evaluate_fold(test_fold)
            scores.append(fold_score)

    return statistics.mean(scores)
```

Scoring criteria example:
- -100 points for invalid SQL
- -1 point per returned row (discourage over-broad queries)
- +5 points per correctly matched row

### System Prompt Customization

For testing prompt variations:
```python
class SqlSystemPrompt:
    def __init__(self, examples: Optional[List[Dict[str, str]]] = None):
        self.examples = examples or load_default_examples()
    
    def build_prompt(self) -> str:
        return f"""
        Given the following schema...
        Examples:
        {self.format_examples()}
        """
```

## Best Practices

1. Unit Testing
   - Use appropriate test models (TestModel vs FunctionModel)
   - Capture and verify message flows
   - Use fixtures for common setups
   - Prevent accidental real model calls

2. Evals
   - Define clear performance metrics
   - Use cross-validation when appropriate
   - Consider multiple evaluation strategies
   - Track performance changes over time
   - Document evaluation criteria
   - Balance accuracy vs. cost/time

3. System Prompts
   - Test variations systematically
   - Use cross-validation for example selection
   - Document prompt changes and effects
   - Consider A/B testing in production