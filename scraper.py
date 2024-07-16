import requests 
import re
import os
import ollama
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def extract_nouns(url, items):
    
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    ingredient_class_regex = re.compile(r'.*ingredient.*', re.IGNORECASE)

    element_regex = re.compile(r'(div|section|article|ul|ol)', re.IGNORECASE)

    ingredient_elements = soup.find_all(element_regex, class_=ingredient_class_regex)
    ingredients = []
    for element in ingredient_elements:
        results = element.find_all("li")
        for result in results:
            ingredients.append(result.text)
    prompt = f"Extract only the nouns from the following ingredient list, :\n{ingredients} if any are similar to the ones in this list please match the exist wording: \n{items} Don't include an introduction \nNouns:"
    response = ollama.generate(model='llama3', prompt=prompt)
    return response['response']
