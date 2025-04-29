"""
Expérimentation YOLO sur base de données de fruits avec variation d'hyperparamètres
et visualisation des résultats avec une heatmap seaborn.
Le modèle est chargé une seule fois pour optimiser le processus.
"""

from ultralytics import YOLO
import torch
import cv2
import os
import glob
import multiprocessing 
import numpy as np
from torch.utils.tensorboard import SummaryWriter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class TBLoggerCallback:
    def __init__(self, writer):
        """
        Initialisation du callback avec TensorBoard writer
        """
        self.writer = writer
    
    def on_fit_epoch_end(self, trainer):
        """
        Fonction appelée à la fin de chaque epoch.
        Elle logue toutes les métriques disponibles.
        """
        epoch = trainer.epoch
        metrics = trainer.metrics

        print(f"\n📊 [Epoch {epoch}] Métriques disponibles :", metrics)

        for key, value in metrics.items():
            if isinstance(value, (int, float)) or hasattr(value, 'item'):
                if hasattr(value, 'item'):
                    value = value.item()  # Convertir les tenseurs en valeurs Python
                self.writer.add_scalar(f"YOLO/{key}", value, epoch)

def train_model(model, mixup_val, copy_paste_val, experiment_name):
    """
    Fonction pour entraîner un modèle avec des valeurs spécifiques de mixup et copy_paste
    Le modèle est déjà chargé et passé en paramètre
    """
    # Configuration du device
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    
    # Conversion des valeurs NumPy en float Python standard
    mixup_val = float(mixup_val)
    copy_paste_val = float(copy_paste_val)
    
    # TensorBoard Writer (log dans runs/yolo_train)
    log_dir = f"runs/yolo_train/passe5/mixup_{mixup_val:.2f}_copypaste_{copy_paste_val:.2f}"
    writer = SummaryWriter(log_dir)

    try:
        # Ajouter le callback TensorBoard
        tb_logger = TBLoggerCallback(writer)
        model.add_callback("on_fit_epoch_end", tb_logger.on_fit_epoch_end)

        # Configuration de l'entraînement avec les augmentations spécifiées
        args = dict(
                data='C:/Users/chauv/Desktop/bdd_3fruits/passe5/conf.yml',
                epochs=2,
                imgsz=640,
                batch=16,
                device=device,
                show=True,
                mosaic=1.0,
                mixup=mixup_val,           # Valeur variable pour mixup
                copy_paste=copy_paste_val, # Valeur variable pour copy_paste
                degrees=20.0,
                translate=0.1,
                scale=0.25,
                shear=0.0,
                perspective=0.0,
                flipud=0.0,
                fliplr=0.5,
                hsv_h=0.015,
                hsv_s=0.7,
                hsv_v=0.4,
                optimizer='adam',
                lr0=0.0001,
                momentum=0.937,
                weight_decay=0.0005,
                save=True,
                project='3fruits',
                name=f'mixup_{mixup_val:.2f}_copypaste_{copy_paste_val:.2f}'
            )

        # === Entraînement ===
        results = model.train(**args)

        # Logging final des hyperparams + métriques YOLO
        metrics = results.metrics if hasattr(results, "metrics") else {}

        # Conversion des métriques pour TensorBoard (éviter les types NumPy)
        metrics_dict = {}
        for k, v in metrics.items():
            if isinstance(v, (int, float)) or hasattr(v, 'item'):
                if hasattr(v, 'item'):
                    v = v.item()  # Convertir les tenseurs en valeurs Python
                metrics_dict[f"hparam/{k}"] = float(v)

        # Convertir également les args pour add_hparams
        hparams_dict = {k: float(v) if isinstance(v, (np.floating, np.integer)) else v 
                        for k, v in args.items() if isinstance(v, (int, float, str, bool, np.floating, np.integer))}
        
        writer.add_hparams(hparams_dict, metrics_dict)
        print(f"📈 Résultats de l'entraînement (mixup={mixup_val}, copy_paste={copy_paste_val}):", results.metrics)
        
        # Supprimer le callback pour éviter les problèmes de duplication
        model.callbacks = {k: cb for k, cb in model.callbacks.items() if cb != tb_logger.on_fit_epoch_end}
        
        return metrics
        
    except Exception as e:
        print(f"⚠️ Erreur pendant l'entraînement: {str(e)}")
        return {"error": str(e)}
    finally:
        writer.close()

def create_seaborn_heatmap(mixup_values, copy_paste_values, results_matrix, output_path):
    """
    Crée une heatmap avec seaborn pour visualiser les résultats de mAP50
    """
    # Créer un DataFrame pandas pour seaborn
    df = pd.DataFrame(
        results_matrix,
        index=[f"{val:.2f}" for val in copy_paste_values],
        columns=[f"{val:.2f}" for val in mixup_values]
    )
    
    # Configurer la figure
    plt.figure(figsize=(10, 8))
    
    # Créer la heatmap avec seaborn
    ax = sns.heatmap(
        df, 
        annot=True,           # Afficher les valeurs numériques
        fmt=".4f",            # Format des valeurs (4 décimales)
        cmap="YlGnBu",        # Palette de couleurs (YlGnBu = jaune-vert-bleu)
        linewidths=0.5,       # Largeur des lignes de séparation
        cbar_kws={'label': 'mAP50'} # Étiquette de la barre de couleur
    )
    
    # Ajouter les titres et les labels
    plt.title("Impact de mixup et copy_paste sur mAP50", fontsize=16)
    plt.xlabel("Mixup", fontsize=14)
    plt.ylabel("Copy-Paste", fontsize=14)
    
    # Ajuster les paramètres de la figure
    plt.tight_layout()
    
    # Enregistrer l'image
    plt.savefig(output_path)
    print(f"✅ Heatmap seaborn enregistrée dans {output_path}")
    
    # Fermer la figure pour libérer la mémoire
    plt.close()

def main():
    # Configuration du device
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    print(f"🖥️ Utilisation du device: {device}")
    
    # Chargement du modèle une seule fois
    print("📦 Chargement du modèle YOLO...")
    model = YOLO('yolo11l.pt')
    print("✅ Modèle chargé avec succès!")

    # Définir les plages de valeurs pour mixup et copy_paste
    mixup_values = np.linspace(0, 1, 5)  # [0.0, 0.25, 0.5, 0.75, 1.0]
    copy_paste_values = np.linspace(0, 1, 5)  # [0.0, 0.25, 0.5, 0.75, 1.0]
    
    # Stockage des résultats
    all_results = {}
    
    # Matrice pour la métrique mAP50
    map50_matrix = np.zeros((len(copy_paste_values), len(mixup_values)))
    
    # Double boucle pour tester toutes les combinaisons
    print("\n🧪 Démarrage des expérimentations...")
    for i, mixup_val in enumerate(mixup_values):
        for j, copy_paste_val in enumerate(copy_paste_values):
            experiment_name = f"mixup_{float(mixup_val):.2f}_copypaste_{float(copy_paste_val):.2f}"
            print(f"\n🔬 Expérience: {experiment_name}")
            
            # Entraînement avec cette combinaison
            metrics = train_model(model, mixup_val, copy_paste_val, experiment_name)
            
            # Stockage des résultats
            all_results[(float(mixup_val), float(copy_paste_val))] = metrics
            
            # Stockage dans la matrice pour la heatmap (mAP50)
            if metrics and 'metrics/mAP50(B)' in metrics:
                map50_matrix[j, i] = float(metrics['metrics/mAP50(B)'])
    
    # Créer le dossier de résultats s'il n'existe pas
    os.makedirs("3fruits/heatmaps", exist_ok=True)
    
    # Sauvegarder les résultats pour référence future
    np.save("3fruits/map50_results.npy", map50_matrix)
    
    # Créer la heatmap seaborn
    create_seaborn_heatmap(mixup_values, copy_paste_values, map50_matrix, "3fruits/heatmaps/map50_seaborn_heatmap.png")
    
    # Affichage des résultats à la fin de toutes les expériences
    print("\n\n📊 Résumé des expériences:")
    for (mixup_val, copy_paste_val), metrics in all_results.items():
        print(f"Mixup: {mixup_val:.2f}, Copy-Paste: {copy_paste_val:.2f}")
        
        # Afficher les métriques principales (mAP50)
        if metrics and 'error' not in metrics:
            if 'metrics/mAP50(B)' in metrics:
                print(f"  mAP50: {metrics['metrics/mAP50(B)']:.4f}")
        else:
            print(f"  ❌ Échec: {metrics.get('error', 'Erreur inconnue')}")
            
        print("-" * 40)
    
    print("\n📊 Une heatmap Seaborn a été générée dans le fichier '3fruits/heatmaps/map50_seaborn_heatmap.png'")

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()