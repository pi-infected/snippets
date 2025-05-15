# AnswerFormat & get_ai_task_answer

This library provides a comprehensive solution for obtaining structured responses from different AI providers (OpenAI, Anthropic, Google Gemini, and Perplexity).

## Features

- Creation of standardized response formats with type validation via Pydantic
- Support for multiple AI providers:
  - OpenAI (ChatGPT)
  - Anthropic (Claude)
  - Google Gemini
  - Perplexity
- Plain text or JSON responses based on needs
- Error handling and retries

## Installation

```bash
pip install openai anthropic google-genai pydantic
```

## Basic Usage

### Response Format with AnswerFormat

```python
from pydantic import Field
from typing import List, Optional
from answer_format import AnswerFormat

# Definition of a simple format
class RecipeFormat(AnswerFormat):
  title: str = Field(..., description="Recipe title")
  ingredients: List[str] = Field(..., description="List of ingredients")
  steps: List[str] = Field(..., description="Preparation steps")
  preparation_time: int = Field(..., description="Preparation time in minutes")
  difficulty: str = Field(..., description="Difficulty level")
  tags: Optional[List[str]] = Field(None, description="Tags associated with the recipe")
```

### Usage with OpenAI

```python
from openai import OpenAI
from answer import get_ai_task_answer

# Client initialization
openai_client = OpenAI(api_key="your-api-key")

# Example with structured format
response = get_ai_task_answer(
  _client=openai_client,
  task="Give me a simple chocolate cake recipe.",
  model="gpt-4o-mini",
  system_prompt="You are an expert chef.",
  answer_format=RecipeFormat,
  provider='openai'
)

print(f"Title: {response.title}")
print(f"Ingredients: {', '.join(response.ingredients)}")
```

### Usage with Anthropic (Claude)

```python
from anthropic import Anthropic
from answer import get_ai_task_answer

# Client initialization
anthropic_client = Anthropic(api_key="your-api-key")

# Example with structured format
response = get_ai_task_answer(
  _client=anthropic_client,
  task="Give me a simple chocolate cake recipe.",
  model="claude-3-7-sonnet-latest",
  provider='anthropic',
  system_prompt="You are an expert chef.",
  answer_format=RecipeFormat,
  max_tokens=1000
)
```

### Usage with Google Gemini

```python
from google import genai
from answer import get_ai_task_answer

# Client initialization
genai_client = genai.Client(api_key="your-api-key")

# Example with structured format
response = get_ai_task_answer(
  _client=genai_client,
  task="Give me a simple chocolate cake recipe.",
  model="gemini-2.0-flash",
  provider='google',
  system_prompt="You are an expert chef.",
  answer_format=RecipeFormat,
  max_tokens=1000
)
```

### Usage with Perplexity

```python
from openai import OpenAI
from answer import get_ai_task_answer

# Client initialization
perplexity_client = OpenAI(
  api_key="your-api-key",
  base_url="https://api.perplexity.ai"
)

# Example with text format
response = get_ai_task_answer(
  _client=perplexity_client,
  task="Give me a simple chocolate cake recipe.",
  model="sonar",
  provider='perplexity',
  system_prompt="You are an expert chef."
)
```

## Advanced Response Formats

### Nested Objects

```python
class ResultItem(AnswerFormat):
  name: str = Field(..., description="Item name")
  description: str = Field(..., description="Detailed description")
  score: Optional[float] = Field(None, description="Evaluation score out of 10")
  
class ComplexFormat(AnswerFormat):
  result: List[ResultItem] = Field(..., description="List of results")
  total_count: int = Field(..., description="Total number of items")
  query_time: float = Field(..., description="Query execution time in seconds")
  category: Optional[str] = Field(None, description="Category of results")
```

### Automatic Example Generation and Prompt Insertion (done automatically by the get_ai_task_answer function)

```python
# Generating an automatic example
example = RecipeFormat.generate_example()
print(example)

# Generating a prompt with format and descriptions
prompt = RecipeFormat.generate_prompt()
print(prompt)
```

## Parameters for get_ai_task_answer

| Parameter | Type | Description |
|-----------|------|-------------|
| _client | object | API Client (OpenAI, Anthropic, Google GenAI, Perplexity) |
| task | str | The task or question to send to the model |
| model | str | The model name to use |
| system_prompt | str | The system prompt to use |
| answer_format | Type[AnswerFormat] | Pydantic class defining the expected response format |
| provider | str | The API provider ('openai', 'perplexity', 'anthropic' or 'google') |
| max_tokens | int | Maximum number of tokens for the response |

## Error Handling

The `get_ai_task_answer` function automatically handles common API errors:
- Authentication errors
- Rate limit errors
- Server errors
- Response format errors

Each error triggers a new attempt up to 3 times before giving up.
