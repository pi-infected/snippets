import json
import re
import json_repair
from fix_busted_json import repair_json

def decode_json_edge_cases(str_json):
  if not str_json or str_json.isspace():
    return None

  try:   
    def clean_json(s):
      # Nettoyer les espaces et commentaires
      s = re.sub(r'//.*?\n|/\*.*?\*/', '', s, flags=re.S)
      s = s.strip()
      
      # Si le JSON est déjà valide, le retourner tel quel
      try:
        return json.loads(s)
      except json.JSONDecodeError:
        pass
      
      # Ajouter des accolades si nécessaire
      if not s.startswith('{') and not s.startswith('['):
        s = '{' + s + '}'

      # Remplacer les valeurs spéciales avant tout traitement
      s = re.sub(r'\bNone\b(?=[\s,\]}]|$)', 'null', s)
      s = re.sub(r'\bTrue\b(?=[\s,\]}]|$)', 'true', s)
      s = re.sub(r'\bFalse\b(?=[\s,\]}]|$)', 'false', s)

      # Traiter le contenu caractère par caractère
      result = []
      i = 0
      in_string = False
      current_quote = None
      escape = False
      buffer = []
      after_colon = False
      value_words = []
      
      while i < len(s):
        char = s[i]
        
        # Gérer l'échappement
        if escape:
          if current_quote:
            buffer.append('\\' + char)
          else:
            result.append('\\' + char)
          escape = False
          i += 1
          continue
          
        if char == '\\':
          escape = True
          i += 1
          continue
        
        # Dans une chaîne
        if in_string:
          if char == current_quote and not escape:
            # Vérifier les guillemets consécutifs
            j = i + 1
            quote_count = 1
            while j < len(s) and s[j] == current_quote:
              quote_count += 1
              j += 1
            
            if quote_count > 1:  # Guillemets multiples
              if quote_count % 2 == 0:  # Nombre pair
                buffer.append('\\"')
                i = j - 1
              else:  # Nombre impair
                in_string = False
                current_quote = None
                if buffer:
                  result.extend(buffer)
                  buffer = []
                result.append('"')
                i = j - 1
            else:  # Un seul guillemet
              in_string = False
              current_quote = None
              if buffer:
                result.extend(buffer)
                buffer = []
              result.append('"')
          else:
            if current_quote == "'":
              if char == '"':
                buffer.append('\\"')
              else:
                buffer.append(char)
            else:
              buffer.append(char)
        
        # Hors d'une chaîne
        else:
          if char in ['"', "'"]:
            in_string = True
            current_quote = char
            if buffer:
              if after_colon:
                value_words.append(''.join(buffer).strip())
              else:
                word = ''.join(buffer).strip()
                result.append(f'"{word}"')
              buffer = []
            result.append('"')
          elif char == ':':
            if buffer:
              word = ''.join(buffer).strip()
              result.append(f'"{word}"')
              buffer = []
            result.append(char)
            after_colon = True
            value_words = []
          elif char in [',', '{', '}', '[', ']']:
            if buffer:
              if after_colon:
                value_words.append(''.join(buffer).strip())
              else:
                word = ''.join(buffer).strip()
                if word == 'null' or word == 'None':
                  result.append('null')
                elif word.lower() == 'true':
                  result.append('true')
                elif word.lower() == 'false':
                  result.append('false')
                elif re.match(r'^[A-Z_]+$', word):
                  result.append(f'"{word}"')
                elif word and not re.match(r'^-?\d+(?:\.\d+)?(?:e-?\d+)?$', word):
                  result.append(f'"{word}"')
                elif word:
                  result.append(word)
              buffer = []
            
            if value_words:
              value = ' '.join(value_words).strip()
              if value == 'null' or value == 'None':
                result.append('null')
              elif value.lower() == 'true':
                result.append('true')
              elif value.lower() == 'false':
                result.append('false')
              elif re.match(r'^[A-Z_]+$', value):
                result.append(f'"{value}"')
              elif value and not re.match(r'^-?\d+(?:\.\d+)?(?:e-?\d+)?$', value):
                result.append(f'"{value}"')
              elif value:
                result.append(value)
              value_words = []
            
            result.append(char)
            after_colon = False
          elif char in [' ', '\n', '\t']:
            if buffer:
              if after_colon:
                value_words.append(''.join(buffer).strip())
              else:
                word = ''.join(buffer).strip()
                if word == 'null' or word == 'None':
                  result.append('null')
                elif word.lower() == 'true':
                  result.append('true')
                elif word.lower() == 'false':
                  result.append('false')
                elif re.match(r'^[A-Z_]+$', word):
                  result.append(f'"{word}"')
                elif word and not re.match(r'^-?\d+(?:\.\d+)?(?:e-?\d+)?$', word):
                  result.append(f'"{word}"')
                elif word:
                  result.append(word)
              buffer = []
            result.append(char)
          else:
            buffer.append(char)
        
        i += 1
      
      # Traiter les buffers restants
      if buffer:
        if after_colon:
          value_words.append(''.join(buffer).strip())
        else:
          word = ''.join(buffer).strip()
          if word == 'null' or word == 'None':
            result.append('null')
          elif word.lower() == 'true':
            result.append('true')
          elif word.lower() == 'false':
            result.append('false')
          elif re.match(r'^[A-Z_]+$', word):
            result.append(f'"{word}"')
          elif word and not re.match(r'^-?\d+(?:\.\d+)?(?:e-?\d+)?$', word):
            result.append(f'"{word}"')
          elif word:
            result.append(word)
      
      if value_words:
        value = ' '.join(value_words).strip()
        if value == 'null' or value == 'None':
          result.append('null')
        elif value.lower() == 'true':
          result.append('true')
        elif value.lower() == 'false':
          result.append('false')
        elif re.match(r'^[A-Z_]+$', value):
          result.append(f'"{value}"')
        elif value and not re.match(r'^-?\d+(?:\.\d+)?(?:e-?\d+)?$', value):
          result.append(f'"{value}"')
        elif value:
          result.append(value)
      
      s = ''.join(result)
      
      # Nettoyer les espaces superflus
      s = re.sub(r'\s+', ' ', s)
      
      return s

    cleaned_json = clean_json(str_json)
    
    try:
      parsed = json.loads(cleaned_json)
    except json.JSONDecodeError as e:
      if "undefined" in str_json or "NaN" in str_json:
        raise ValueError(f"Invalid JSON value: undefined or NaN not allowed")
      raise
    
    def convert_nulls(obj):
      if isinstance(obj, dict):
        return {k: convert_nulls(v) for k, v in obj.items()}
      elif isinstance(obj, list):
        return [convert_nulls(x) for x in obj]
      elif obj is None:
        return None
      return obj
    
    return convert_nulls(parsed)
    
  except json.JSONDecodeError:
    raise json.JSONDecodeError()

none_patterns = [
  r'([^\\]":\s*)None([,\s}]|$)',
  r'(\[|\,\s*)None\s*([,\]\n]|$)',
  r'({\s*)None\s*([,}\n]|$)'
]

def fix_multiline_strings(str_json):
  corrected_str_json = re.sub(r'{\s+', r'{', str_json, re.MULTILINE)
  corrected_str_json = re.sub(r'\s+}', r'}', corrected_str_json, re.MULTILINE)
  corrected_str_json = re.sub(r'\s*"\s*', r'"', corrected_str_json, re.MULTILINE)
  corrected_str_json = re.sub(r'[^\S\n]+\n', r'\n', corrected_str_json, re.MULTILINE)
  corrected_str_json = re.sub(r'[^\S\n]+\n', r'\n', corrected_str_json, re.MULTILINE)
  corrected_str_json = corrected_str_json.replace('\n', '\\n')
  return corrected_str_json

def decode_json(str_json):
  try:
    return json.loads(str_json)
  except json.JSONDecodeError:
    pass
  
  original_str_json = str_json
  
  str_json = str_json.strip()
  open_brackets = str_json.count('{')
  close_brackets = str_json.count('}')
  
  if open_brackets > close_brackets:
    str_json = str_json + '}'*(open_brackets - close_brackets)
    close_brackets += 1
  elif close_brackets > open_brackets:
    str_json = "{ "*(close_brackets - open_brackets) + str_json
    open_brackets += 1
    
  if not str_json.startswith('{') and open_brackets > 0:
    str_json = "{" + "{".join(str_json.split("{")[1:])
  elif open_brackets == 0:
    str_json = "{" + str_json
    
  if not str_json.endswith('}') and close_brackets > 0:
    str_json = "}".join(str_json.split("}")[:-1]) + "}"
  elif close_brackets == 0:
    str_json = str_json + "}"
    
  multiline_unfixed_str_json = str_json
  str_json = fix_multiline_strings(str_json)
  relatively_fixed_str_json = str_json
  
  try:
    return json.loads(relatively_fixed_str_json)
  except:
    try:
      return json.loads(multiline_unfixed_str_json)
    except:
      # Remplacer les ' par " autour des variables
      new_json = re.sub(r"'([^'\s]*)':", r'"\1":', multiline_unfixed_str_json)
      
      # Remplacer les "None" par "null"
      for pattern in none_patterns:
        new_json = re.sub(pattern, lambda m: m.group(1) + 'null' + m.group(2), new_json)
        
      try:
        return json.loads(new_json)
      except:
        try:
          return json.loads(str_json)
        except json.JSONDecodeError:
          try:
            return decode_json_edge_cases(original_str_json)
          except:
            try:
              return decode_json_edge_cases(multiline_unfixed_str_json)
            except:
              try:
                return decode_json_edge_cases(relatively_fixed_str_json)
              except:
                try:
                  return json_repair.loads(original_str_json, skip_json_loads=True)
                except:
                  try:
                    return json_repair.loads(relatively_fixed_str_json, skip_json_loads=True)
                  except:
                    try:
                      return json_repair.loads(str_json, skip_json_loads=True)
                    except:
                      return repair_json(original_str_json)