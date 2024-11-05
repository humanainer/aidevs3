import os
from dotenv import load_dotenv
import requests

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

# Stałe
TASK_NAME = "POLIGON"
AGENTAPI = os.getenv('AGENTAPI')  # Pobierz AGENTAPI z pliku .env
DATA_URL = "https://poligon.aidevs.pl/dane.txt"
VERIFY_URL = "https://poligon.aidevs.pl/verify"

# Pobierz dane z URL
response = requests.get(DATA_URL)
strings = response.text.strip().split('\n')

# Przygotuj payload do weryfikacji
payload = {
    "task": TASK_NAME,
    "apikey": AGENTAPI,  # Użyj zmiennej AGENTAPI
    "answer": strings
}

# Wyślij odpowiedź
verify_response = requests.post(VERIFY_URL, json=payload)
print(verify_response.json())