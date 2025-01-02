"""
Sauvegarde de la base de données MongoDB dans un fichier JSON,
afin d'exploitation des données par Eric
Ce code estfonctionnel
"""

from pymongo import MongoClient
import json
import os
from datetime import datetime
# Connexion à la base de données
client = MongoClient('mongodb://localhost:27017/')
db = client['0safe-cook']

# Créer un dossier pour la sauvegarde
now = datetime.now( )
timestamp = now.strftime("%d-%m-%Y")
backup_dir = f"backup_safe_cook_json/timestamp {timestamp}"
os.makedirs(backup_dir, exist_ok=True)


# Exporter chaque collection
for collection_name in db.list_collection_names():
    collection = db[collection_name]
    
    # Récupérer tous les documents
    documents = list(collection.find({}))
    
    # Créer le fichier de sauvegarde
    output_file = os.path.join(backup_dir, f"{collection_name}.json")
    
    # Sauvegarder en JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(documents, f, default=str, ensure_ascii=False, indent=2)
    
    print(f"Collection {collection_name} sauvegardée dans {output_file}")

print(f"\nSauvegarde terminée! Tous les fichiers sont dans le dossier: {backup_dir}")