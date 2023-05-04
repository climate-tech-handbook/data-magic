from app import app
from loader import load_dotenv, openai, os
from app.models.content_generator import ContentGenerator

load_dotenv()

unsplash_access_key = os.getenv("UNSPLASH_ACCESS_KEY")

if unsplash_access_key is None:
    print("Error: UNSPLASH_ACCESS_KEY environment variable is not set.")


api_key = os.getenv("OPENAI_SECRET_KEY")

if api_key is None:
    print(
        "Error: OPENAI_SECRET_KEY environment variable is not set. OpenAI API key needed to make requests."
    )
    exit(1)
