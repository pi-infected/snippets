# The pi-infected Python snippets

A collection of scripts that solve real problems I've encountered in my work.

## What's in this collection?

This repository contains solutions to various programming challenges and tasks I've had to tackle. Each script is designed to be reusable and adaptable to similar situations.

### Current Scripts:

#### AI Response Generation (`ai/task`)
A comprehensive solution for obtaining structured responses from various AI providers:

- **Provider-independent interface**: Works with OpenAI, Anthropic (Claude), Google Gemini, and Perplexity
- **Complete API error handling**: Automatically retries up to 3 times in case of errors
- **Any Python object generation**: Simply define your class with Pydantic to get properly structured objects with high success rate thanks to JSON generation
- **Robust JSON error recovery**: Excellent recovery rate for malformed JSON responses
- **Plain text support**: Can also be used to produce simple text responses

The library provides a unified way to interact with AI models without worrying about the underlying API differences or error handling.
