"""
test pour verifier que les images sont bien annotées 

mettre en argument le fruit a tester
    -apple
    -orange
    -banana

"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import random
import sys

def plot_random_images_with_boxes(images_dir, labels_dir, rows=5, cols=5, fruit=None):
    # Obtenir tous les fichiers d'images
    image_files = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    # S'assurer qu'il y a assez d'images
    if len(image_files) < rows * cols:
        print(f"Attention: seulement {len(image_files)} images disponibles, moins que les {rows*cols} demandées")
        rows = min(rows, len(image_files))
        cols = min(cols, len(image_files) // rows + (1 if len(image_files) % rows else 0))
    
    # Sélectionner des images aléatoirement
    selected_images = random.sample(image_files, rows * cols)
    
    # Créer une figure avec des subplots
    fig, axes = plt.subplots(rows, cols, figsize=(15, 15))
    
    # Aplatir le tableau d'axes si nécessaire (pour le cas 1×1)
    if rows == 1 and cols == 1:
        axes = np.array([axes])
    
    axes = axes.flatten()
    
    for i, img_file in enumerate(selected_images):
        # Construire les chemins
        base_name = os.path.splitext(img_file)[0]
        img_path = os.path.join(images_dir, img_file)
        label_path = os.path.join(labels_dir, f"{base_name}.txt")
        
        # Vérifier que l'image et le label existent
        if not os.path.exists(img_path):
            print(f"Image {img_file} introuvable")
            continue
            
        if not os.path.exists(label_path):
            print(f"Label pour {img_file} introuvable")
            # On peut quand même afficher l'image sans annotations
        
        # Lire l'image
        image = cv2.imread(img_path)
        if image is None:
            print(f"Impossible de charger l'image {img_file}")
            continue
            
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, _ = image.shape
        
        # Lire et dessiner les bounding boxes si le label existe
        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                lines = f.readlines()
            
            for line in lines:
                data = line.strip().split()
                if len(data) >= 5:  # S'assurer qu'il y a assez de données
                    class_id = int(data[0])
                    x_center = float(data[1]) * width
                    y_center = float(data[2]) * height
                    box_width = float(data[3]) * width
                    box_height = float(data[4]) * height
                    
                    # Calculer les coordonnées du rectangle
                    x1 = int(x_center - box_width / 2)
                    y1 = int(y_center - box_height / 2)
                    x2 = int(x_center + box_width / 2)
                    y2 = int(y_center + box_height / 2)
                    
                    # Dessiner le rectangle (vert pour être bien visible)
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    
                    # Ajouter l'étiquette de classe
                    cv2.putText(image, f'{class_id} {fruit}', (x1, y1-10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Afficher l'image dans le subplot
        axes[i].imshow(image)
        axes[i].set_title(f"{img_file[:10]}...")  # Titre court
        axes[i].axis('off')  # Cacher les axes
    
    plt.tight_layout()
    plt.show()


# important pour le chemin des images, choisir le fruit
fruit = sys.argv[1].lower()

# Utilisation avec votre chemin
folder_path = f'D:/00_DataBase_safecook/safecook_img_database/{fruit}/train/'
images_dir = f"{folder_path}images/"
labels_dir = f"{folder_path}labels/"


# Afficher une grille 5×5 d'images aléatoires avec leurs annotations
plot_random_images_with_boxes(images_dir, labels_dir, rows=5, cols=5,fruit=fruit)