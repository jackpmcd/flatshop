import requests 
import re
import os
import ollama
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')

url = input("Enter the URL of the recipe: ")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

ingredient_class_regex = re.compile(r'.*ingredient.*', re.IGNORECASE)

element_regex = re.compile(r'(div|section|article|ul|ol)', re.IGNORECASE)

ingredient_elements = soup.find_all(element_regex, class_=ingredient_class_regex)

def extract_nouns(ingredient_list):
    prompt = f"Extract only the nouns from the following ingredient list:\n{ingredient_list}\nNouns:"
    response = ollama.generate(model='llama3', prompt=prompt)
    return response['response']

ingredients = []
for element in ingredient_elements:
    results = element.find_all("li")
    for result in results:
        ingredients.append(result.text)

nouns = extract_nouns(ingredients)
print(nouns)