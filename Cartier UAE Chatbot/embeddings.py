from google import genai
from config import GEMINI_API_KEY

# Initialize Gemini client for embeddings.
gemini_client = genai.Client(api_key=GEMINI_API_KEY)


def get_embedding(text: str) -> list:
    """
    Generate embeddings for a given text using Gemini's text-embedding-004 model.
    """
    try:
        response = gemini_client.models.embed_content(
            model="text-embedding-004", contents=[text]
        )
        # Assume the response returns a list of embeddings; pick the first one.
        embedding = response.embeddings[0].values
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []
