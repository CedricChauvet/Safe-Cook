"""
Structure de la page d'une recette Marmiton:
- Titre
- Note et nombre d'avis
- Temps de préparation
- Difficulté
- Coût

et c'est tout pour l'instant
"""

import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class MarmitonRecipe:
    title: str
    rating: Optional[float]
    review_count: int
    prep_time: str
    difficulty: str
    cost: str
    servings: int
    ingredients: List[str]
    steps: List[str]
    tips: List[str]
    tags: List[str]
    url: str

def get_recipe_details(url: str) -> Optional[MarmitonRecipe]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extraction du titre
        title = soup.find('h1').text.strip()
        
        # Extraction de la note et nombre d'avis
        rating = None
        review_count = 0
        rating_div = soup.find('div', class_='recipe-header__rating')
        if rating_div:
            rating_text = rating_div.find('span', class_='recipe-header__rating-text')
            if rating_text:
                rating = float(rating_text.text.strip().replace('/5', ''))
            review_count_elem = rating_div.find('span', class_='recipe-header__rating-count')
            if review_count_elem:
                review_count = int(''.join(filter(str.isdigit, review_count_elem.text)))
        
        # Extraction du temps de préparation
        time_total = soup.find(class_="time__total")
        if time_total:
            # Récupérer le texte du span (label)
            time_label = time_total.find('span')
            # Récupérer le texte du div (valeur)
            time_value = time_total.find('div').text.strip()
            prep_time = time_value


       # Récupérer le conteneur recipe-primary
        recipe_primary = soup.find('div', class_='recipe-primary')
        if recipe_primary:
            # Chercher tous les items à l'intérieur de recipe-primary
            recipe_items = recipe_primary.find_all('div', class_='recipe-primary__item')
            
            # Parcourir les items pour trouver la difficulté et le coût
            for item in recipe_items:
                # Vérifier si l'item contient une icône
                icon = item.find('i', class_='icon')
                if icon:
                    # Récupérer le span correspondant
                    span_text = item.find('span').text if item.find('span') else ""
                    
                    # Identifier le type d'information selon l'icône
                    if 'icon-difficulty' in icon['class']:
                        difficulty = span_text
                    elif 'icon-price' in icon['class']:
                        cost = span_text


        # Extraction du nombre de portions Non fonctionnel
        # servings = 0
        # portion_elements = soup.find_all(class_=lambda x: x and ('quantity' in x.lower() or 'portion' in x.lower()))
        # print("Éléments trouvés :")
        # for elem in portion_elements:
        #     print(f"\nClasse : {elem.get('class')}")
        #     print(f"Contenu : {elem.text.strip()}")
        

        
        return MarmitonRecipe(
            title=title,
            rating=rating,
            review_count=review_count,
            prep_time=prep_time,
            difficulty=difficulty,
            cost=cost,
            servings=-1,
            ingredients=None,
            steps=None,
            tips=None,
            tags=None,
            url=url
        )
        
    except Exception as e:
        print(f"Erreur lors de l'extraction de la recette: {e}")
        return None

# Test
def print_recipe(recipe: MarmitonRecipe):
    if not recipe:
        print("Impossible de récupérer la recette")
        return
        
    print(f"Titre: {recipe.title}")
    print(f"Note: {recipe.rating}/5 ({recipe.review_count} avis)")
    print(f"Temps de préparation: {recipe.prep_time}")
    print(f"Difficulté: {recipe.difficulty}")
    print(f"Coût: {recipe.cost}")
    print(f"Nombre de portions: {recipe.servings}")
    
    # print("\nIngrédients:")
    # for ingredient in recipe.ingredients:
    #     print(f"- {ingredient}")
    
    # print("\nÉtapes:")
    # for i, step in enumerate(recipe.steps, 1):
    #     print(f"{i}. {step}")
    
    # if recipe.tips:
    #     print("\nAstuces:")
    #     for tip in recipe.tips:
    #         print(f"- {tip}")
    
    # if recipe.tags:
    #     print("\nTags:")
    #     print(", ".join(recipe.tags))

url = "https://www.marmiton.org/recettes/recette_pates-a-la-carbonara_80453.aspx"
recipe = get_recipe_details(url)
print_recipe(recipe)