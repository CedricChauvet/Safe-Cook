"""
Vérification du modèle YOLO

Ce script teste le chargement d'un modèle YOLO via la librairie ultralytics,
affiche les informations basiques du modèle, et gère les erreurs éventuelles.
"""

import os
import sys
import traceback
from ultralytics import YOLO


def test_yolo_model(model_path: str) -> bool:
    """
    Teste le chargement d'un modèle YOLO et affiche des informations sur le modèle.

    Args:
        model_path (str): Chemin vers le fichier du modèle YOLO (.pt)

    Returns:
        bool: True si le modèle a été chargé avec succès, False sinon.
    """
    print(f"Démarrage du test pour le modèle : {model_path}")

    # Vérifier si le fichier du modèle existe
    file_exists = os.path.exists(model_path)
    print(f"Le fichier existe : {file_exists}")

    if file_exists:
        file_size_mb = os.path.getsize(model_path) / (1024 * 1024)
        print(f"Taille du fichier : {file_size_mb:.2f} MB")

    try:
        print("Chargement du modèle YOLO en cours...")
        model = YOLO(model_path)
        print("Modèle chargé avec succès !\n")

        # Affichage des informations principales du modèle
        print("--- Résumé du modèle ---")
        print(f"Type du modèle : {type(model)}")
        print(f"Noms des classes : {model.names}")
        print(f"Nombre de classes : {len(model.names)}")

        # Essayer d'afficher le nombre de paramètres si possible
        if hasattr(model, 'model'):
            try:
                num_params = sum(p.numel() for p in model.model.parameters())
                print(f"Nombre de paramètres : {num_params:,}")
            except Exception:
                print("Impossible de récupérer le nombre de paramètres du modèle.")

        print("--- Fin du résumé ---")
        return True

    except Exception as error:
        print(f"ERREUR lors du chargement du modèle : {error}")
        print("Traceback détaillé :")
        print(traceback.format_exc())
        return False


if __name__ == "__main__":
    # Chemin par défaut vers le modèle
    model_file_path = "yolobest4.pt"

    # Si un argument est passé en ligne de commande, l'utiliser comme chemin
    if len(sys.argv) > 1:
        model_file_path = sys.argv[1]

    # Affichage des versions Python et ultralytics
    print(f"Version Python : {sys.version}")
    ultralytics_version = getattr(YOLO, '__version__', 'inconnue')
    print(f"Version Ultralytics : {ultralytics_version}")

    # Lancer le test de chargement du modèle
    is_successful = test_yolo_model(model_file_path)

    if is_successful:
        print("\nTest réussi : le modèle a été chargé correctement.")
    else:
        print("\nTest échoué : impossible de charger le modèle.")
        sys.exit(1)  # Quitter avec un code d'erreur
