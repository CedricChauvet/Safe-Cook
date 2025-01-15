from ultralytics import YOLO
import torch
from pathlib import Path

def train_yolo(
    data_yaml_path: str,
    yolo_weights: str = "yolov8x.pt",
    epochs: int = 100,
    imgsz: int = 640,
    batch_size: int = 16,
    device: str = "0"  # "0" pour premier GPU, "" pour CPU
):
    """
    Fine-tune YOLOv8 sur un dataset personnalisé
    
    Args:
        data_yaml_path: Chemin vers le fichier data.yaml
        yolo_weights: Chemin vers les poids pré-entraînés ou nom du modèle
        epochs: Nombre d'époques d'entraînement
        imgsz: Taille des images en entrée
        batch_size: Taille du batch
        device: Device à utiliser ("0", "0,1", "cpu", etc.)
    """
    # Vérification du GPU
    if torch.cuda.is_available() and device:
        print(f"Utilisation du GPU: {torch.cuda.get_device_name(0)}")
    else:
        print("Utilisation du CPU")
        device = "cpu"

    # Chargement du modèle
    model = YOLO(yolo_weights)
    
    # Configuration de l'entraînement
    training_args = {
        'data': data_yaml_path,         # chemin vers data.yaml
        'epochs': epochs,               # nombre d'époques
        'imgsz': imgsz,                # taille des images
        'batch': batch_size,           # taille du batch
        'device': device,              # device à utiliser
        'workers': 8,                  # nombre de workers pour le chargement des données
        'patience': 50,                # early stopping patience
        'save': True,                  # sauvegarder les meilleurs modèles
        'save_period': 10,            # sauvegarder tous les N époques
        'cache': False,               # cache des images en RAM
        'pretrained': True,           # utiliser les poids pré-entraînés
        'optimizer': 'auto',          # optimiseur à utiliser
        'verbose': True,              # afficher les logs détaillés
        'seed': 42,                   # seed pour reproductibilité
        'resume': False,              # reprendre un entraînement
        'val': True,                  # faire la validation
    }
    
    # Lancement de l'entraînement
    try:
        results = model.train(**training_args)
        print("Entraînement terminé avec succès!")
        
        # Affichage des métriques finales
        print("\nMétriques finales:")
        metrics = results.results_dict
        print(f"mAP50: {metrics.get('metrics/mAP50(B)', 'N/A'):.3f}")
        print(f"mAP50-95: {metrics.get('metrics/mAP50-95(B)', 'N/A'):.3f}")
        
        return results, model
        
    except Exception as e:
        print(f"Erreur pendant l'entraînement: {str(e)}")
        return None, None

def evaluate_model(model, data_yaml_path: str, imgsz: int = 640):
    """
    Évalue le modèle sur le dataset de validation
    """
    try:
        results = model.val(data=data_yaml_path, imgsz=imgsz)
        print("\nRésultats de l'évaluation:")
        print(f"mAP50: {results.results_dict['metrics/mAP50(B)']:.3f}")
        print(f"mAP50-95: {results.results_dict['metrics/mAP50-95(B)']:.3f}")
        return results
    except Exception as e:
        print(f"Erreur pendant l'évaluation: {str(e)}")
        return None

if __name__ == "__main__":
    # Configuration
    DATA_YAML = "C:/Users/chauv/Desktop/Safe-Cook/bdd_aliments_yolo/datasets/LVIS_fruit_vegetables/data.yaml"
    YOLO_WEIGHTS = "yolo11x.pt"  # ou chemin vers vos poids personnalisés
    
    # Paramètres d'entraînement
    EPOCHS = 100
    IMG_SIZE = 640
    BATCH_SIZE = 16
    DEVICE = "0"  # Utilisez "" pour CPU
    
    # Lancement de l'entraînement
    print("Début du fine-tuning...")
    results, model = train_yolo(
        data_yaml_path=DATA_YAML,
        yolo_weights=YOLO_WEIGHTS,
        epochs=EPOCHS,
        imgsz=IMG_SIZE,
        batch_size=BATCH_SIZE,
        device=DEVICE
    )
    
    if model is not None:
        # Évaluation du modèle
        print("\nÉvaluation du modèle...")
        eval_results = evaluate_model(model, DATA_YAML, IMG_SIZE)