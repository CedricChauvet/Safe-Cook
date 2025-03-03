import requests
import base64
import json

def detect_objects(image_path):
    """
    Envoyer une image et récupérer les classes détectées
    Attention detect object existe dans le serveur et le client
    """
    try:
        # Encoder l'image en base64
        with open(image_path, 'rb') as image_file:
            image_b64 = base64.b64encode(image_file.read()).decode('utf-8')

        print(image_b64[:100:])
        
        # Envoyer la requête, est ce qu'on peut envoyer autre chose
        # dans la requete? user id, etc?
        # response = requests.post('http://localhost:5000/detect', 
                
        url = 'https://servicesafecook-981813095604.europe-west9.run.app/detect'
        headers = {'Content-type': 'application/json'}  # Important de spécifier le Content-Type
        data = json.dumps({'image': image_b64})  # Conversion explicite en JSON
        
        response = requests.post(url, data=data, headers=headers, timeout=30)  # Timeout pour éviter les blocages
        # response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP (4xx, 5xx)
        
        # response = requests.post('https://169.254.8.1/detect', 
        #     json={'image': image_b64}
        # )
        
        # Vérifier le statut de la répo
        # nse. Si 200, OK
        if response.status_code != 200:
            print("Erreur du serveur:")
            print(response.json())
            return []
        
        return response.json()
    
    except Exception as e:
        print("Erreur de connexion ou de traitement:")
        print(e)
        return []

# Exemple d'utilisation
if __name__ == '__main__':
    image_path = "./images/brocoli.jpeg"
    result = detect_objects(image_path)
    
    if result:
        print("Classes détectées :", result.get('classes', []))
        print("Nombre d'instances par classe :", result.get('class_counts', {}))