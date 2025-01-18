import requests
from bs4 import BeautifulSoup
import re

def get_marmiton_aspx_urls(base_url):
    aspx_urls = []
    page = 1
    
    for i in range(1):
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        links = soup.find_all('a', href=re.compile(r'\.aspx$'))
        if not links:
            break
        
        for link in links:
            aspx_urls.append(base_url + link['href'])
        
        page += 1
    
    return aspx_urls

base_url = "https://www.marmiton.org/recettes/recherche.aspx?aqt=tomate-basilic-fromage&st=1"
aspx_urls = get_marmiton_aspx_urls(base_url)

for url in aspx_urls:
    print(url)