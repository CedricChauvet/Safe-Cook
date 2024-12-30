"""
ce code recuypere des information les etapes de préparation de la recette
il est fonctionnel
"""
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List, Optional

def extract_recipe_steps(html_content):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(html_content, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    steps = soup.find_all('div', class_='recipe-step-list__container')
    
    recipe_steps = []
    for step in steps:
        text = step.find('p').text.strip()
        recipe_steps.append(text)
    
    return recipe_steps

# Usage
html_content = "https://www.marmiton.org/recettes/recette_pates-a-la-carbonara_80453.aspx"
steps = extract_recipe_steps(html_content)
print(steps)
# Affichage des étapes en print
# for i, step in enumerate(steps, 1):
#     print(f"Étape {i}: {step}")


