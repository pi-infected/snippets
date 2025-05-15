from pydantic import BaseModel
from typing import Dict, Any, Union, get_type_hints, get_origin, get_args
import inspect
import json

class AnswerFormat(BaseModel):
  """Classe de base pour définir le format de réponse attendu d'un modèle d'IA"""
  
  @classmethod
  def from_json(cls, json_data: Dict[str, Any]):
    """Crée une instance à partir d'un dictionnaire JSON"""
    return cls(**json_data)
  
  def to_dict(self) -> Dict[str, Any]:
    """Convertit l'instance en dictionnaire"""
    return self.model_dump()
  
  @classmethod
  def generate_example(cls) -> Dict[str, Any]:
    """Génère un exemple basé sur les descriptions des champs"""
    example = {}
    model_fields = cls.model_fields
    
    for field_name, field_info in model_fields.items():
      field_type = get_type_hints(cls).get(field_name)
      description = field_info.description or "Valeur d'exemple"
      example_value = AnswerFormat._generate_example_value(field_type, description)
      example[field_name] = example_value
    
    return example
  
  @staticmethod
  def _generate_example_value(field_type: Any, description: str) -> Any:
    """Génère une valeur d'exemple en fonction du type"""
    # Gérer les types optionnels (Optional[X])
    origin = get_origin(field_type)
    args = get_args(field_type)
    
    if origin is Union and type(None) in args:
      # C'est un Optional, on prend le premier type qui n'est pas None
      inner_type = next(arg for arg in args if arg is not type(None))
      return AnswerFormat._generate_example_value(inner_type, description)
    
    # Gérer les listes (List[X])
    if origin is list:
      inner_type = args[0] if args else Any
      # Pour les listes, on retourne deux éléments d'exemple
      return [
        AnswerFormat._generate_example_value(inner_type, description + " 1"),
        AnswerFormat._generate_example_value(inner_type, description + " 2")
      ]
    
    # Gérer les dictionnaires (Dict[K, V])
    if origin is dict:
      key_type, value_type = args if len(args) == 2 else (Any, Any)
      return {
        AnswerFormat._generate_example_value(key_type, "Clé"): 
        AnswerFormat._generate_example_value(value_type, f"Valeur pour {description}")
      }
    
    # Gérer les sous-classes de AnswerFormat
    try:
      if inspect.isclass(field_type) and issubclass(field_type, AnswerFormat):
        # Si c'est une sous-classe de AnswerFormat, utiliser sa méthode generate_example
        return field_type.generate_example()
    except TypeError:
      # Si field_type n'est pas une classe, issubclass lèvera TypeError
      pass
    
    # Gérer les types de base
    if field_type is str:
      return f"Exemple de {description}"
    elif field_type is int:
      return 42
    elif field_type is float:
      return 3.14
    elif field_type is bool:
      return True
    
    # Pour les types complexes, retourner une chaîne simple
    return f"Exemple de {description}"
  
  @classmethod
  def generate_prompt(cls) -> str:
    """Génère un exemple de format JSON à insérer dans un prompt"""
    example = cls.generate_example()
    example_json = json.dumps(example, indent=2, ensure_ascii=False)
    
    field_descriptions = []
    AnswerFormat._add_field_descriptions(cls, "", field_descriptions)
    
    prompt = f"""Réponds en suivant strictement ce format JSON:
{example_json}

Description des champs:
{"".join(f"{desc}\n" for desc in field_descriptions)}
"""
    return prompt

  @staticmethod
  def _add_field_descriptions(cls, prefix: str, field_descriptions: list):
    """Ajoute récursivement les descriptions des champs y compris pour les objets imbriqués"""
    for field_name, field_info in cls.model_fields.items():
      field_type = get_type_hints(cls).get(field_name)
      field_path = f"{prefix}.{field_name}" if prefix else field_name
      desc = field_info.description or f"Valeur pour {field_path}"
      field_descriptions.append(f"- {field_path}: {desc}")
      
      # Ajouter les descriptions pour les champs imbriqués
      try:
        origin = get_origin(field_type)
        args = get_args(field_type)
        
        # Pour les champs optionnels (Union[Type, None])
        if origin is Union and type(None) in args:
          inner_type = next(arg for arg in args if arg is not type(None))
          field_type = inner_type
        
        # Pour les types imbriqués
        if inspect.isclass(field_type) and issubclass(field_type, AnswerFormat):
          AnswerFormat._add_field_descriptions(field_type, field_path, field_descriptions)
      except (TypeError, AttributeError):
        # Si field_type n'est pas une classe ou n'a pas les attributs requis
        pass