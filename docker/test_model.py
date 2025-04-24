import os
import sys
import traceback
from ultralytics import YOLO

def test_yolo_model(model_path):
    print(f"Début du test de chargement du modèle: {model_path}")
    print(f"Vérification de l'existence du fichier: {os.path.exists(model_path)}")
    
    if os.path.exists(model_path):
        print(f"Taille du fichier: {os.path.getsize(model_path) / (1024 * 1024):.2f} MB")
    
    try:
        print("Tentative de chargement du modèle...")
        model = YOLO(model_path)
        print("Modèle chargé avec succès!")
        
        # Afficher des informations sur le modèle
        print("\n--- Résumé du modèle ---")
        print(f"Type de modèle: {type(model)}")
        print(f"Noms de classes disponibles: {model.names}")
        print(f"Nombre de classes: {len(model.names)}")
        
        # Afficher les paramètres du modèle si disponibles
        if hasattr(model, 'model'):
            try:
                num_params = sum(p.numel() for p in model.model.parameters())
                print(f"Nombre de paramètres: {num_params:,}")
            except:
                print("Impossible d'obtenir le nombre de paramètres")
        
        print("--- Fin du résumé ---")
        return True
    
    except Exception as e:
        print(f"ERREUR lors du chargement du modèle: {e}")
        print("Détails de l'erreur:")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    # Chemin du modèle (utilisez le chemin où se trouve votre modèle)
    model_path = "yolobest4.pt"
    
    # Si un argument est fourni, utilisez-le comme chemin
    if len(sys.argv) > 1:
        model_path = sys.argv[1]
    
    print(f"Python version: {sys.version}")
    print(f"Ultralytics version: {YOLO.__version__ if hasattr(YOLO, '__version__') else 'inconnu'}")
    
    # Tester le chargement du modèle
    success = test_yolo_model(model_path)
    
    if success:
        print("\nTest réussi: Le modèle a été chargé correctement.")
    else:
        print("\nTest échoué: Impossible de charger le modèle.")
        sys.exit(1)  # Sortie avec code d'erreur