from pymongo import MongoClient
import json
from bson import ObjectId
import os
from datetime import datetime

# Connexion à la base de données
client = MongoClient('mongodb://localhost:27017/')
db = client['0safe-cook']

# Créer un dossier pour la sauvegarde
# timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
backup_dir = f"backup_0safe_cook_db"
os.makedirs(backup_dir, exist_ok=True)

# Classe pour gérer la sérialisation des ObjectId
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

# Exporter chaque collection
for collection_name in db.list_collection_names():
    collection = db[collection_name]
    
    # Récupérer tous les documents
    documents = list(collection.find({}))
    
    # Créer le fichier de sauvegarde
    output_file = os.path.join(backup_dir, f"{collection_name}.json")
    
    # Sauvegarder en JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(documents, f, cls=JSONEncoder, ensure_ascii=False, indent=2)
    
    print(f"Collection {collection_name} sauvegardée dans {output_file}")

print(f"\nSauvegarde terminée! Tous les fichiers sont dans le dossier: {backup_dir}")