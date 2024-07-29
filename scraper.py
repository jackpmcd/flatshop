import requests 
import re
import os
from openai import OpenAI
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def extract_nouns(url, items):
    
    page = requests.get(url, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    ingredient_class_regex = re.compile(r'.*ingredient.*', re.IGNORECASE)

    element_regex = re.compile(r'(div|section|article|ul|ol|data-testid)', re.IGNORECASE)

    ingredient_elements = soup.find_all(element_regex, class_=ingredient_class_regex)
    ingredients = []
    for element in ingredient_elements:
        results = element.find_all("li")
        for result in results:
            ingredients.append(result.text)

    if len(ingredients) == 0:
        return "broken"
    
    ingredients_str = " ".join(ingredients)
    items_str = " ".join(items)
    
    client = OpenAI()
    custom_messages=[
            {"role": "assistant", "content": "You are a helpful assistant."},
            {"role": "user", "content": "DO NOT HAVE AN INTRODUCTION SENTENCE! Extract only the ingredients from this list, remove any measurements, keep compound ingredients together (i.e. ground pepper, basmati rice, fresh parsley): " + ingredients_str} 
        ]
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = custom_messages    
    )

    response = completion.choices[0].message
    if len(items) > 0:
        custom_messages = []
        custom_messages.append({"role": "assistant", "content": response.content})
        custom_messages.append({"role": "user", "content": "DO NOT HAVE AN INTRODUCTION SENTENCE! If any ingredients are similar to the ones in this list please match the exist wording, leave all the other ingredients as they are: " + items_str})

        completion2 = client.chat.completions.create(
            model="gpt-4o-mini",
            messages = custom_messages
        )

        response2 = completion2.choices[0].message
        return response2.content

    else:
        return response.content 
