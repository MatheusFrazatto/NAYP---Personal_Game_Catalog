import requests
import os
from dotenv import load_dotenv


class RawgAPI:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("RAWG_API_KEY")
        self.base_url = "https://api.rawg.io/api/games"

        if not self.api_key:
            raise ValueError(
                "API key not found. Please set the RAWG_API_KEY environment variable.")

    def search_game(self, game_name):
        parameters = {
            "key": self.api_key,
            "search": game_name
        }
        response = requests.get(self.base_url, params=parameters)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def full_game_details(self, game_id):
        url = f"https://api.rawg.io/api/games/{game_id}"
        params = {'key': self.api_key}

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Erro ao buscar detalhes do jogo: {e}")
            return None
