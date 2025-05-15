from openai import OpenAI
from pydantic import Field
from typing import List, Optional
from anthropic import Anthropic
from google import genai

from answer import get_ai_task_answer
from answer_format import AnswerFormat

# Clés API stockées en variables (à remplacer par les vôtres)
OPENAI_API_KEY = '<votre clé API OpenAI>'
PERPLEXITY_API_KEY = '<votre clé API Perplexity>'
GOOGLE_GENAI_API_KEY = '<votre clé API Google GenAI>'
ANTHROPIC_API_KEY = '<votre clé API Anthropic>'

# Définition d'un format de réponse spécifique avec Pydantic
class RecipeFormat(AnswerFormat):
  title: str = Field(..., description="Titre de la recette")
  ingredients: List[str] = Field(..., description="Liste des ingrédients")
  steps: List[str] = Field(..., description="Étapes de préparation")
  preparation_time: int = Field(..., description="Temps de préparation en minutes")
  difficulty: str = Field(..., description="Niveau de difficulté")
  tags: Optional[List[str]] = Field(None, description="Tags associés à la recette")

# Définition d'un format plus complexe avec des objets imbriqués
class ResultItem(AnswerFormat):
  name: str = Field(..., description="Nom de l'élément")
  description: str = Field(..., description="Description détaillée")
  score: Optional[float] = Field(None, description="Score d'évaluation sur 10")
  
class ComplexFormat(AnswerFormat):
  result: List[ResultItem] = Field(..., description="Liste des résultats")
  total_count: int = Field(..., description="Nombre total d'éléments")
  query_time: float = Field(..., description="Temps d'exécution de la requête en secondes")
  category: Optional[str] = Field(None, description="Catégorie des résultats")

def test_openai():
  """Test avec OpenAI"""
  try:
    # Initialisation du client
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    
    # Exemple avec format structuré
    print("\n=== Test OpenAI avec format structuré ===")
    response = get_ai_task_answer(
      _client=openai_client,
      task="Donne-moi une recette de gâteau au chocolat simple.",
      model="gpt-4o-mini",
      system_prompt="Tu es un chef cuisinier expert.",
      answer_format=RecipeFormat,
      provider='openai'
    )
    
    print(f"Titre: {response.title}")
    print(f"Ingrédients: {', '.join(response.ingredients)}")
    print(f"Temps de préparation: {response.preparation_time} minutes")
    print(f"Difficulté: {response.difficulty}")
    
    # Exemple avec texte brut
    print("\n=== Test OpenAI avec texte brut ===")
    response_text = get_ai_task_answer(
      _client=openai_client,
      task="Donne-moi une recette de gâteau au chocolat simple.",
      model="gpt-4o-mini",
      system_prompt="Tu es un chef cuisinier expert. Sois concis.",
      provider='openai'
    )
    
    print(response_text)
  except Exception as e:
    print(f"⚠️ Test OpenAI non exécuté: {e}")
    print("Vérifiez votre clé API ou votre connexion internet.")

def test_openai_complex_format():
  """Test avec OpenAI et un format de données complexe"""
  try:
    # Initialisation du client
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    
    print("\n=== Test OpenAI avec format complexe ===")
    response = get_ai_task_answer(
      _client=openai_client,
      task="Génère une liste de 3 films de science-fiction populaires avec leurs descriptions.",
      model="gpt-4o-mini",
      system_prompt="Tu es un expert en cinéma.",
      answer_format=ComplexFormat,
      provider='openai'
    )
    
    print(f"Nombre total: {response.total_count}")
    print(f"Temps de requête: {response.query_time} secondes")
    print(f"Catégorie: {response.category}")
    print("\nRésultats:")
    
    for i, item in enumerate(response.result, 1):
      print(f"\nRésultat {i}:")
      print(f"  Nom: {item.name}")
      print(f"  Description: {item.description}")
      if item.score:
        print(f"  Score: {item.score}/10")
  except Exception as e:
    print(f"⚠️ Test OpenAI format complexe non exécuté: {e}")
    print("Vérifiez votre clé API ou votre connexion internet.")

def test_perplexity():
  """Test avec Perplexity et le modèle sonar"""
  try:
    # Initialisation du client
    perplexity_client = OpenAI(
      api_key=PERPLEXITY_API_KEY,
      base_url="https://api.perplexity.ai"
    )
    
    # Exemple avec Perplexity en format json
    print("\n=== Test Perplexity avec réponse json ===")
    response = get_ai_task_answer(
      _client=perplexity_client,
      task="Donne-moi une recette de gâteau au chocolat simple.",
      model="sonar",  # Modèle Perplexity
      provider='perplexity',
      system_prompt="Tu es un chef cuisinier expert.",
      answer_format=RecipeFormat
    )
    
    print(f"Titre: {response.title}")
    print(f"Ingrédients: {', '.join(response.ingredients)}")
    print(f"Temps de préparation: {response.preparation_time} minutes")
    print(f"Difficulté: {response.difficulty}")
    
    # Exemple avec Perplexity mais en essayant d'obtenir du texte brut
    print("\n=== Test Perplexity avec format simple ===")
    try:
      response = get_ai_task_answer(
        _client=perplexity_client,
        task="Donne-moi une recette de gâteau au chocolat simple.",
        model="sonar",
        provider='perplexity',
        system_prompt="Tu es un chef cuisinier expert."
      )
      
      print(f"Réponse: {response}")
    except Exception as e:
      print(f"Erreur lors de la conversion en format structuré: {e}")
  except Exception as e:
    print(f"⚠️ Test Perplexity non exécuté: {e}")
    print("Vérifiez votre clé API ou votre connexion internet.")

def test_anthropic():
  """Test avec Anthropic et Claude"""
  try:
    # Initialisation du client
    anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)
    
    # Exemple avec Anthropic en format json
    print("\n=== Test Anthropic avec réponse json ===")
    response = get_ai_task_answer(
      _client=anthropic_client,
      task="Donne-moi une recette de gâteau au chocolat simple.",
      model="claude-3-7-sonnet-latest",
      provider='anthropic',
      system_prompt="Tu es un chef cuisinier expert.",
      answer_format=RecipeFormat,
      max_tokens=1000
    )
    
    print(f"Titre: {response.title}")
    print(f"Ingrédients: {', '.join(response.ingredients)}")
    print(f"Temps de préparation: {response.preparation_time} minutes")
    print(f"Difficulté: {response.difficulty}")
    
    # Exemple avec Anthropic mais en texte brut
    print("\n=== Test Anthropic avec format texte ===")
    try:
      response = get_ai_task_answer(
        _client=anthropic_client,
        task="Donne-moi une recette de gâteau au chocolat simple en moins de 100 mots.",
        model="claude-3-7-sonnet-latest",
        provider='anthropic',
        system_prompt="Tu es un chef cuisinier expert. Sois concis.",
        max_tokens=500
      )
      
      print(f"Réponse: {response}")
    except Exception as e:
      print(f"Erreur lors de l'utilisation d'Anthropic en texte brut: {e}")
  except Exception as e:
    print(f"⚠️ Test Anthropic non exécuté: {e}")
    print("Vérifiez votre clé API ou votre connexion internet.")

def test_google_genai():
  """Test avec Google GenAI et Gemini"""
  try:
    # Initialisation du client
    genai_client = genai.Client(api_key=GOOGLE_GENAI_API_KEY)
    
    # Exemple avec Google GenAI en format json
    print("\n=== Test Google GenAI avec réponse json ===")
    response = get_ai_task_answer(
      _client=genai_client,
      task="Donne-moi une recette de gâteau au chocolat simple.",
      model="gemini-2.0-flash",
      provider='google',
      system_prompt="Tu es un chef cuisinier expert.",
      answer_format=RecipeFormat,
      max_tokens=1000
    )
    
    print(f"Titre: {response.title}")
    print(f"Ingrédients: {', '.join(response.ingredients)}")
    print(f"Temps de préparation: {response.preparation_time} minutes")
    print(f"Difficulté: {response.difficulty}")
    
    # Exemple avec Google GenAI mais en texte brut
    print("\n=== Test Google GenAI avec format texte ===")
    try:
      response = get_ai_task_answer(
        _client=genai_client,
        task="Donne-moi une recette de gâteau au chocolat simple en moins de 100 mots.",
        model="gemini-2.0-flash",
        provider='google',
        system_prompt="Tu es un chef cuisinier expert. Sois concis.",
        max_tokens=500
      )
      
      print(f"Réponse: {response}")
    except Exception as e:
      print(f"Erreur lors de l'utilisation de Google GenAI en texte brut: {e}")
  except Exception as e:
    print(f"⚠️ Test Google GenAI non exécuté: {e}")
    print("Vérifiez votre clé API ou votre connexion internet.")

def test_generate_examples():
  """Teste la génération d'exemples et de prompts"""
  # Afficher un exemple du format généré et le prompt
  print("=== Prompt généré à partir du modèle RecipeFormat ===")
  format_prompt = RecipeFormat.generate_prompt()
  print(format_prompt)
  
  print("\n=== Prompt généré à partir du format complexe ===")
  format_complex_prompt = ComplexFormat.generate_prompt()
  print(format_complex_prompt)

if __name__ == "__main__":
  # Tests de génération d'exemples (ne nécessite pas de clés API)
  test_generate_examples()
  
  # Tests avec les différents fournisseurs (chaque test peut être exécuté indépendamment)
  print("\n=== Tests avec OpenAI ===")
  test_openai()
  
  print("\n=== Tests avec format complexe ===")
  test_openai_complex_format()
  
  print("\n=== Tests avec Perplexity ===")
  test_perplexity()
  
  print("\n=== Tests avec Anthropic ===")
  test_anthropic()
  
  print("\n=== Tests avec Google GenAI ===")
  test_google_genai()
