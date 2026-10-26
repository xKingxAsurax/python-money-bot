import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    print("Tentando publicar tweet de prueba...")
    try:
        client = tweepy.Client(
            consumer_key=os.getenv("X_API_KEY"),
            consumer_secret=os.getenv("X_API_SECRET"),
            access_token=os.getenv("X_ACCESS_TOKEN"),
            access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET")
        )
        response = client.create_tweet(text="SISTEMA ACTIVO 🚀 EcoOfertasBot en linea y funcionando!")
        print(f"¡ÉXITO! Tweet publicado. ID: {response.data['id']}")
    except Exception as e:
        print(f"Error fatal: {e}")

if __name__ == "__main__":
    test_connection()
