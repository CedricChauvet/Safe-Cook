import requests
import base64
import sys
import numpy as np

def detect_objects(image_path):
    """
    Envoyer une image et récupérer les classes détectées
    """
    try:
        # Encoder l'image en base64
        with open(image_path, 'rb') as image_file:
            image_b64 = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Envoyer la requête
        response = requests.post('http://localhost:5000/detect', 
            json={'image': image_b64}
        )
        
        # Vérifier le statut de la réponse
        if response.status_code != 200:
            print("Erreur du serveur:")
            print(response.json())
            return []
        
        return response.json()['classes']
    
    except Exception as e:
        print("Erreur de connexion ou de traitement:")
        print(e)
        return []

# Exemple d'utilisation
if __name__ == '__main__':
    
    image_path = "./images/image5.jpg"
    response = detect_objects(image_path)
        # Afficher les classes détectées
    print("Classes détectées :", response[1])
    
    # Afficher le nombre d'instances par classe
    #print("Nombre d'instances par classe :", response.get('class_counts', {}))