import torch
import cv2
import os
import numpy as np
import uuid
import base64
from flask import Flask, request, jsonify
import traceback
from ultralytics import YOLO
from collections import Counter

app = Flask(__name__)


# Charger le modèle au démarrage
try:
    model = YOLO("yolo11x.pt")
    print("Modèle YOLO chargé avec succès")
except Exception as e:
    print("Erreur fatale lors du chargement du modèle :")
    print(traceback.format_exc())
    model = None


@app.route('/detect', methods=['POST'])
def detect_objects():
    """
    Endpoint pour la détection de classes d'objets
    """
    if model is None:
        return jsonify({
            'error': 'Modèle YOLO non chargé',
            'details': 'Échec du chargement initial du modèle'
        }), 500

    if 'image' not in request.json:
        return jsonify({'error': 'Pas d\'image fournie'}), 400

    try:
        # Décoder l'image base64
        image_b64 = request.json['image']

        # Enlever le préfixe data:image si présent
        if image_b64.startswith('data:image'):
            # Extraire uniquement la partie base64 après la virgule
            image_b64 = image_b64.split(',')[1]

        print("Image reçue, décodage en cours...")
        # Décoder
        image_bytes = base64.b64decode(image_b64)
        image_np = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

        # Vérification et resize
        if image is None:
            raise ValueError("Échec du décodage de l'image")
            
        # image = cv2.resize(image, (640, 640))
        image = make_square_with_padding(image)





        # Vérification de l'image
        if image is None:
            return jsonify({
                'error': 'Impossible de décoder l\'image',
                'details': 'La conversion en image a échoué'
            }), 500

        # Définir le chemin vers le répertoire monté
        # c'est le chemin du conteneur

        # # Générer un nom de fichier unique avec UUID
        # unique_id = str(uuid.uuid4())
        # filename = f"{unique_id}.jpg"
        # filepath = os.path.join(UPLOAD_DIR, filename)
        # # Sauvegarder l'image originale sous format uuid
        # with open(filepath, 'wb') as f:
        #     f.write(image_bytes)

        # Conversion en tensor
        image_tensor = torch.from_numpy(image).permute(2, 0, 1).float() / 255.0
        image_tensor = image_tensor.unsqueeze(0)

        # Détecter les objets, bien choisir le seuil de confiance
        results = model(image_tensor, conf=0.5)

        # Traitement des détections
        detections = []
        classes = []
        boxes = []
        confidences = []
        labels = []
        
        for box in results[0].boxes:
            class_name = model.names[int(box.cls)]
            confidence = float(box.conf.item())
            bbox = box.xyxy[0]  # Format: x1, y1, x2, y2
            
            classes.append(class_name)
            detections.append((class_name, confidence))
            boxes.append(bbox)
            confidences.append(confidence)
            labels.append(class_name)
            
        class_counts = dict(Counter(classes))

        # Générer un nom de fichier unique
        unique_id = uuid.uuid4()


        image_with_boxes = draw_detections(
            image, 
            torch.stack(boxes), 
            labels, 
            confidences
        )

        UPLOAD_DIR = '/mount'

        filename = f"{unique_id}_with_boxes.jpg"
        filepath = os.path.join(UPLOAD_DIR, filename)
        cv2.imwrite(str(filepath), image_with_boxes)


        # partie renvoyée au client
        # classes : liste des classes détectées
        # class_counts : nombre d'instances par classe
        # filename : nom du fichier sauvegardé
        # peut on ajouter autre chose?
        return jsonify({
            'classes': classes,
            'class_counts': class_counts,
            'filename': filename
        })

    except Exception as e:
        # Imprimer l'erreur complète côté serveur
        print("Erreur lors de la détection :")
        print(traceback.format_exc())

        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


def make_square_with_padding(image):
    """
    Transforme une image en image carrée en ajoutant des bordures noires.
    L'image d'origine conserve ses proportions.
    
    Args:
        image: Image source (format numpy array / OpenCV)
    
    Returns:
        Image carrée avec bordures noires
    """
    # Obtenir les dimensions de l'image
    height, width = image.shape[:2]
    
    # Déterminer la taille du carré (prendre le plus grand côté)
    square_size = max(height, width)
    
    # Créer une image carrée noire
    square_image = np.zeros((square_size, square_size, 3), dtype=np.uint8)
    
    # Calculer les offsets pour centrer l'image
    x_offset = (square_size - width) // 2
    y_offset = (square_size - height) // 2
    
    # Copier l'image originale au centre
    square_image[y_offset:y_offset+height, x_offset:x_offset+width] = image
    
    return square_image


def draw_detections(
    image,
    boxes,
    labels,
    confidences
) -> np.ndarray:
    """
    Dessine les boîtes de détection et les étiquettes sur l'image.
    
    Args:
        image: Image numpy
        boxes: Tenseur des boîtes de détection (x1, y1, x2, y2)
        labels: Liste des noms de classes
        confidences: Liste des scores de confiance
    
    Returns:
        Image avec les détections dessinées
    """
    img_with_boxes = image.copy()
    
    for box, label, conf in zip(boxes, labels, confidences):
        # Coordonnées de la boîte
        x1, y1, x2, y2 = map(int, box.tolist())
        
        # Couleur aléatoire pour chaque classe
        color = tuple(np.random.randint(0, 255, 3).tolist())
        
        # Dessiner la boîte
        cv2.rectangle(img_with_boxes, (x1, y1), (x2, y2), color, 2)
        
        # Préparer le texte
        text = f"{label} {conf:.2f}"
        
        # Obtenir les dimensions du texte
        (text_width, text_height), _ = cv2.getTextSize(
            text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
        )
        
        # Dessiner le fond du texte
        cv2.rectangle(
            img_with_boxes,
            (x1, y1 - text_height - 10),
            (x1 + text_width + 10, y1),
            color,
            -1
        )
        
        # Ajouter le texte
        cv2.putText(
            img_with_boxes,
            text,
            (x1 + 5, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )
    
    return img_with_boxes


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
