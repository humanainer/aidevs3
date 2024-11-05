import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import openai
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

# Załaduj zmienne środowiskowe z pliku .env
load_dotenv()

# Ustaw swój klucz API OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

# URL strony, którą chcemy odwiedzić
url = "https://xyz.ag3nts.org/"

# Wysyłanie żądania GET do strony
response = requests.get(url)

# Sprawdzenie, czy żądanie się powiodło
if response.status_code == 200:
    # Parsowanie zawartości strony za pomocą BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Znalezienie elementu z pytaniem na stronie
    question_element = soup.find(string="Prove that you are not human").find_next()
    
    # Wyświetlenie pytania, jeśli zostało znalezione
    if question_element:
        question = question_element.text
        print("Question:", question)
        
        # Wysyłanie pytania do modelu OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # użycie modelu GPT-4o
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{question} Please provide only the year as a number."}
            ],
            max_tokens=10  # ograniczenie liczby tokenów w odpowiedzi
        )
        
        # Uzyskanie odpowiedzi z modelu OpenAI
        answer = response.choices[0].message['content'].strip()
        print("Answer:", answer)
        
        # Użycie Selenium do otwarcia przeglądarki Chrome
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")  # Otwórz przeglądarkę w trybie pełnoekranowym
        service = Service('/usr/local/bin/chromedriver')  # Upewnij się, że ścieżka do chromedriver jest poprawna
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            # Przejdź do strony głównej
            driver.get("https://xyz.ag3nts.org")

            # Poczekaj na załadowanie pól logowania
            wait = WebDriverWait(driver, 10)
            username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
            password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))

            # Wprowadź dane logowania
            username_field.send_keys(os.getenv('USERNAME01'))
            password_field.send_keys(os.getenv('PASSWORD01'))
            password_field.send_keys(Keys.RETURN)

            # Poczekaj na załadowanie strony po zalogowaniu
            wait.until(EC.presence_of_element_located((By.NAME, "answer")))

            # Znajdź i wypełnij pole answer
            answer_field = driver.find_element(By.NAME, "answer")
            answer_field.clear()  # Wyczyść pole przed wprowadzeniem nowej wartości
            answer_field.send_keys(answer)  # Wprowadź odpowiedź z OpenAI

            # Znajdź i kliknij przycisk logowania
            login_button = driver.find_element(By.XPATH, "//button[text()='Login']")
            login_button.click()

            # Przeszukiwanie strony w poszukiwaniu flagi
            page_source = driver.page_source
            potential_flags = re.findall(r'FLAG\{.*?\}', page_source)

            # Wyświetlenie znalezionych flag
            if potential_flags:
                for flag in potential_flags:
                    print("Znaleziono flagę:", flag)
            else:
                print("Nie znaleziono flagi.")

        except Exception as e:
            # Obsługa błędów
            print(f"Wystąpił błąd: {e}")

        # Zatrzymaj skrypt, aby przeglądarka pozostała otwarta
        input("Press Enter to continue...")

    else:
        # Komunikat, jeśli nie znaleziono pytania
        print("Nie znaleziono pytania.")
else:
    # Komunikat o błędzie, jeśli żądanie się nie powiodło
    print("Błąd podczas pobierania strony:", response.status_code)
