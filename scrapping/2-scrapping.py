"""
2-scrapping.py
trouves les etapes de préparation du plat


"""

import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List, Optional



def get_recipe_steps(url: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extraction du titre
    title = soup.find('h1').text.strip()
    print(title)

    
    


   








# Test
url = "https://www.marmiton.org/recettes/recette_pates-a-la-carbonara_80453.aspx"
get_recipe_steps(url)


