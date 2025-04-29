
"""
annotations
"""
import os
import yaml

# Code pour sauvegarder les images de test annotées
def save_annotated_test_images(model, data_yaml, output_dir='test_annotated'):
    """
    Fonction pour sauvegarder les images de test avec les annotations prédites
    
    Args:
        model: Modèle YOLO entraîné
        data_yaml: Chemin vers le fichier de configuration YAML
        output_dir: Répertoire de sortie pour les images annotées
    """
    print("\nSauvegarde des images de test annotées...")
    
    # Création du répertoire de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)
    
    # Obtenir le chemin du répertoire de test à partir du YAML
 
    with open(data_yaml, 'r') as f:
        data_config = yaml.safe_load(f)
    
    # Chemin du répertoire de test
    base_dir = os.path.dirname(data_yaml)
    test_dir = os.path.join(base_dir, data_config.get('test', 'test/images'))
    
    # Récupération de toutes les images de test
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp']
    test_images = []
    for ext in image_extensions:
        test_images.extend(glob.glob(os.path.join(test_dir, ext)))
    
    print(f"Traitement de {len(test_images)} images de test...")
    
    # Traitement de chaque image de test
    for img_path in test_images:
        # Prédiction avec le modèle
        results = model.predict(img_path, conf=0.25, iou=0.45, save=False)
        
        # Récupération de l'image annotée
        annotated_img = results[0].plot()
        
        # Nom du fichier de sortie
        output_filename = os.path.join(output_dir, os.path.basename(img_path))
        
        # Sauvegarde de l'image annotée
        cv2.imwrite(output_filename, annotated_img)
    
    print(f"Images annotées sauvegardées dans le répertoire: {output_dir}")

# Appel de la fonction pour sauvegarder les images de test annotées
save_annotated_test_images(
    model,
    data_yaml='/home/cedrix/Bureau/holbertonschool-demoday/bdd_3fruits/safecook_img_database/conf.yml',
    output_dir='test_annotated'
)

