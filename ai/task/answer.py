from utils import decode_json
import openai
from time import sleep
from answer_format import AnswerFormat
from typing import Optional, Union, Dict, Any, Type
from anthropic import APITimeoutError, AuthenticationError, RateLimitError, APIError
import json
from google.genai import types
from google import genai

def get_ai_task_answer(
  _client, task, model="gpt-4o-mini", 
  system_prompt: str = "Tu es un assistant IA",
  answer_format: Optional[Type[AnswerFormat]] = None, 
  provider: str = 'openai',
  max_tokens: Optional[int] = None
) -> Union[Dict[str, Any], str, AnswerFormat]:
  """
  Obtient une réponse d'un modèle d'IA selon le format spécifié.
  
  Args:
      _client: Client API (OpenAI, Perplexity, Anthropic ou Google GenAI)
      task: La tâche ou question à envoyer au modèle
      model: Le nom du modèle à utiliser
      json_output: Si True, demande une réponse au format JSON
      system_prompt: Le prompt système à utiliser
      answer_format: Classe Pydantic définissant le format de réponse attendu
      provider: Le fournisseur de l'API ('openai', 'perplexity', 'anthropic' ou 'google')
      max_tokens: Nombre maximum de tokens pour la réponse
  
  Returns:
      La réponse du modèle selon le format spécifié
  """
  # Préparer le prompt avec le format demandé si nécessaire
  format_prompt = ""
  if answer_format and not isinstance(answer_format, str):
    format_prompt = answer_format.generate_prompt()
    task = f"{task}\n\n{format_prompt}"
  
  if answer_format:
    json_output = True
  else:
    json_output = False
  
  # Configuration et appel API en fonction du provider
  if provider in ['openai', 'perplexity']:
    return _handle_openai_request(_client, task, model, json_output, system_prompt, answer_format, provider, max_tokens)
  elif provider == 'anthropic':
    return _handle_anthropic_request(_client, task, model, json_output, system_prompt, answer_format, max_tokens)
  elif provider == 'google':
    return _handle_google_request(_client, task, model, json_output, system_prompt, answer_format, max_tokens)
  else:
    raise ValueError(f"Provider non pris en charge: {provider}")

def _handle_openai_request(
  client, task, model, json_output, system_prompt, answer_format, provider, max_tokens
):
  messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": task}
  ]
  
  try_left = 3
  while try_left > 0:
    try:
      params = {
        "model": model,
        "messages": messages
      }
      
      if max_tokens:
        params["max_tokens"] = max_tokens
      
      if json_output and provider == 'openai':
        params["response_format"] = {"type": "json_object"}
        
      response = client.chat.completions.create(**params)
      
      if hasattr(response, 'choices') and response.choices:
        content = response.choices[0].message.content
        
        if not json_output:
          return content
          
        try:
          json_data = decode_json(content)
          if answer_format and not isinstance(answer_format, str):
            return answer_format.from_json(json_data)
          else:
            return json_data
        except Exception as e:
          print(f"Réponse ne respecte pas le format JSON attendu: {e}")
          try_left -= 1
          continue
      else:
        raise Exception("Réponse invalide")
    
    except openai.AuthenticationError as e:
      print(f"API request was not authorized: {e}")
      error_str = str(e).lower()
      if "insufficient_quota" in error_str or "exceeded your current quota" in error_str:
        print(f"Erreur de crédit insuffisant: {e}")
      return None
      
    except openai.RateLimitError as e:
      print(f"API request exceeded rate limit: {e}")
      sleep(60)
      
    except openai.APIError as e:
      print(f"API returned an API Error: {e}")
      sleep(10)
      
    except Exception as e:
      print(f"An exception occurred: {type(e).__name__}: {e}")
      sleep(1)

    try_left -= 1
    
  raise Exception("Erreur lors de l'utilisation de l'API après 3 tentatives")

def _handle_anthropic_request(
  client, task, model, json_output, system_prompt, answer_format, max_tokens
):
  messages = [{"role": "user", "content": task}]
  
  try_left = 3
  while try_left > 0:
    try:
      params = {
        "model": model,
        "system": system_prompt,
        "messages": messages,
        "stream": False
      }
      
      if max_tokens:
        params["max_tokens"] = max_tokens
        
      response = client.messages.create(**params)
      
      if response and response.content:
        content = response.content[0].text
        
        if not json_output:
          return content
          
        try:
          json_data = decode_json(content)
          if answer_format and not isinstance(answer_format, str):
            return answer_format.from_json(json_data)
          else:
            return json_data
        except Exception as e:
          print(f"Réponse ne respecte pas le format JSON attendu: {e}")
          try_left -= 1
          continue
      else:
        raise Exception("Réponse invalide")
        
    except APITimeoutError as e:
      print(f"Timeout lors de la requête Anthropic: {e}")
      sleep(30)
    except AuthenticationError as e:
      print(f"Erreur d'authentification Anthropic: {e}")
      return None
    except RateLimitError as e:
      print(f"Rate limit Anthropic atteint: {e}")
      sleep(60)
    except APIError as e:
      error_str = str(e).lower()
      if "500" in error_str or "529" in error_str or "overloaded_error" in error_str:
        print(f"Erreur serveur Anthropic détectée ({error_str}), nouvelle tentative...")
        sleep(30)
      elif "credit balance is too low" in error_str or "billing" in error_str:
        print(f"Erreur de crédit Anthropic insuffisant: {e}")
        return None
      else:
        print(f"Erreur API Anthropic: {e}")
        sleep(10)
    except Exception as e:
      print(f"Erreur inattendue lors de l'appel à Anthropic: {e}")
      sleep(1)
    
    try_left -= 1
  
  raise Exception("Erreur lors de l'utilisation de l'API Anthropic après 3 tentatives")

def _handle_google_request(
  client, task, model, json_output, system_prompt, answer_format, max_tokens
):
  params = {}
  
  if json_output:
    params['response_mime_type'] = 'application/json'
  
  if system_prompt:
    params['system_instruction'] = system_prompt
    
  if max_tokens:
    params['max_output_tokens'] = max_tokens
    
  params['temperature'] = 0.7
  params['top_p'] = 0.7
  
  try_left = 3
  while try_left > 0:
    try:
      response = client.models.generate_content(
        model=model,
        contents=task,
        config=types.GenerateContentConfig(**params),
      )
      
      if response and response.text:
        content = response.text
        
        if not json_output:
          return content
          
        try:
          json_data = decode_json(content)
          if answer_format and not isinstance(answer_format, str):
            return answer_format.from_json(json_data)
          else:
            return json_data
        except Exception as e:
          print(f"Réponse ne respecte pas le format JSON attendu: {e}")
          try_left -= 1
          continue
      else:
        raise Exception("Réponse invalide")
        
    except Exception as e:
      error_str = str(e).lower()
      if "429" in error_str or "resource_exhausted" in error_str:
        print(f"Rate limit atteint (429), nouvelle tentative dans 60 secondes...")
        sleep(60)
      elif "400" in error_str and "failed_precondition" in error_str:
        print(f"Erreur de crédit Gemini insuffisant: {e}")
        return None
      else:
        print(f"Une erreur est survenue : {type(e).__name__}: {e}")
        sleep(1)
        
      try_left -= 1
  
  raise Exception("Erreur lors de l'utilisation de l'API Google après 3 tentatives")
