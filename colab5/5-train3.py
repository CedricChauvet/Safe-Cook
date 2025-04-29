"""
Du coup créer une heatmap des metrique mAP50
affiche le minimum mAP50 sur èà epochs
affiche aussi le numero d'epoch de ce minima

utilise tensorboard et sns.heatmap  sur un graph de 7*7

resultat
log_dir = f"runs/yolo_train/passe5_49/mixup_{mixup_val:.2f}_copypaste_{copy_paste_val:.2f}"

code Claude, il faut le tester, le documenter 
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
        # Pour suivre la valeur minimale de mAP50 et l'epoch correspondant
        self.min_map50 = float('inf')
        self.min_map50_epoch = -1
    
    def on_fit_epoch_end(self, trainer):
        """
        Fonction appelée à la fin de chaque epoch.
        Elle logue toutes les métriques disponibles et suit le minimum mAP50.
        """
        epoch = trainer.epoch
        metrics = trainer.metrics

        print(f"\n📊 [Epoch {epoch}] Métriques disponibles :", metrics)

        # Vérifier si mAP50 est présent et mettre à jour le minimum si nécessaire
        if 'metrics/mAP50(B)' in metrics:
            current_map50 = metrics['metrics/mAP50(B)'].item() if hasattr(metrics['metrics/mAP50(B)'], 'item') else metrics['metrics/mAP50(B)']
            
            # Mettre à jour le minimum si nécessaire
            if current_map50 < self.min_map50:
                self.min_map50 = current_map50
                self.min_map50_epoch = epoch
                
            # Loguer le min_map50 et l'epoch correspondant
            self.writer.add_scalar(f"YOLO/min_mAP50", self.min_map50, epoch)
            self.writer.add_scalar(f"YOLO/min_mAP50_epoch", self.min_map50_epoch, epoch)

        # Loguer toutes les métriques
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
    log_dir = f"runs/yolo_train/passe5_49/mixup_{mixup_val:.2f}_copypaste_{copy_paste_val:.2f}"
    writer = SummaryWriter(log_dir)
    
    # Pour stocker les informations de minimum mAP50
    min_map50 = float('inf')
    min_map50_epoch = -1

    try:
        # Ajouter le callback TensorBoard
        tb_logger = TBLoggerCallback(writer)
        model.add_callback("on_fit_epoch_end", tb_logger.on_fit_epoch_end)

        # Configuration de l'entraînement avec les augmentations spécifiées
        args = dict(
                data='C:/Users/chauv/Desktop/bdd_3fruits/passe5/conf.yml',
                epochs=70,  # Modifié à 70 epochs
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

        # Récupérer les informations de minimum mAP50 depuis le callback
        min_map50 = tb_logger.min_map50
        min_map50_epoch = tb_logger.min_map50_epoch

        # Logging final des hyperparams + métriques YOLO
        metrics = results.metrics if hasattr(results, "metrics") else {}

        # Ajouter les informations de minimum mAP50 aux métriques
        metrics['min_map50'] = min_map50
        metrics['min_map50_epoch'] = min_map50_epoch

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
        print(f"📉 Minimum mAP50: {min_map50:.4f} à l'epoch {min_map50_epoch}")
        
        # Supprimer le callback pour éviter les problèmes de duplication
        model.callbacks = {k: cb for k, cb in model.callbacks.items() if cb != tb_logger.on_fit_epoch_end}
        
        return metrics
        
    except Exception as e:
        print(f"⚠️ Erreur pendant l'entraînement: {str(e)}")
        return {"error": str(e)}
    finally:
        writer.close()

def create_seaborn_heatmap(mixup_values, copy_paste_values, results_matrix, results_epoch_matrix, output_path):
    """
    Crée une heatmap avec seaborn pour visualiser les résultats de mAP50 minimum
    et le numéro d'epoch correspondant
    """
    # Créer des DataFrames pandas pour seaborn
    df_map50 = pd.DataFrame(
        results_matrix,
        index=[f"{val:.2f}" for val in copy_paste_values],
        columns=[f"{val:.2f}" for val in mixup_values]
    )
    
    df_epochs = pd.DataFrame(
        results_epoch_matrix,
        index=[f"{val:.2f}" for val in copy_paste_values],
        columns=[f"{val:.2f}" for val in mixup_values]
    )
    
    # Créer une figure avec deux subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Créer la heatmap pour mAP50 min
    sns.heatmap(
        df_map50, 
        annot=True,           
        fmt=".4f",            
        cmap="YlGnBu",        
        linewidths=0.5,       
        cbar_kws={'label': 'min mAP50'}, 
        ax=ax1
    )
    ax1.set_title("Minimum mAP50 durant l'entraînement", fontsize=16)
    ax1.set_xlabel("Mixup", fontsize=14)
    ax1.set_ylabel("Copy-Paste", fontsize=14)
    
    # Créer la heatmap pour les epochs correspondants
    sns.heatmap(
        df_epochs, 
        annot=True,           
        fmt="d",              # Format entier pour les numéros d'epochs
        cmap="Oranges",       # Palette différente pour distinguer
        linewidths=0.5,       
        cbar_kws={'label': 'Numéro epoch'}, 
        ax=ax2
    )
    ax2.set_title("Epoch du minimum mAP50", fontsize=16)
    ax2.set_xlabel("Mixup", fontsize=14)
    ax2.set_ylabel("Copy-Paste", fontsize=14)
    
    # Titre global
    plt.suptitle("Impact de mixup et copy_paste sur le minimum mAP50 (70 epochs)", fontsize=18)
    
    # Ajuster les paramètres de la figure
    plt.tight_layout(rect=[0, 0, 1, 0.96])  # Pour laisser de la place au titre global
    
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
    mixup_values = np.linspace(0, 1, 7)  # [0.0, 0.25, 0.5, 0.75, 1.0]
    copy_paste_values = np.linspace(0, 1, 7)  # [0.0, 0.25, 0.5, 0.75, 1.0]
    
    # Stockage des résultats
    all_results = {}
    
    # Matrices pour les métriques
    min_map50_matrix = np.zeros((len(copy_paste_values), len(mixup_values)))
    min_map50_epoch_matrix = np.zeros((len(copy_paste_values), len(mixup_values)), dtype=int)
    
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
            
            # Stockage dans les matrices pour les heatmaps
            if metrics and 'min_map50' in metrics and 'min_map50_epoch' in metrics:
                min_map50_matrix[j, i] = float(metrics['min_map50'])
                min_map50_epoch_matrix[j, i] = int(metrics['min_map50_epoch'])
    
    # Créer le dossier de résultats s'il n'existe pas
    os.makedirs("3fruits/heatmaps", exist_ok=True)
    
    # Sauvegarder les résultats pour référence future
    np.save("3fruits/min_map50_results.npy", min_map50_matrix)
    np.save("3fruits/min_map50_epoch_results.npy", min_map50_epoch_matrix)
    
    # Créer la heatmap seaborn avec les deux informations
    create_seaborn_heatmap(
        mixup_values, 
        copy_paste_values, 
        min_map50_matrix, 
        min_map50_epoch_matrix, 
        "3fruits/heatmaps/min_map50_seaborn_heatmap.png" # on a une image sauvegardée
    )
    
    # Affichage des résultats à la fin de toutes les expériences
    print("\n\n📊 Résumé des expériences:")
    for (mixup_val, copy_paste_val), metrics in all_results.items():
        print(f"Mixup: {mixup_val:.2f}, Copy-Paste: {copy_paste_val:.2f}")
        
        # Afficher les métriques principales
        if metrics and 'error' not in metrics:
            if 'metrics/mAP50(B)' in metrics:
                print(f"  mAP50 final: {metrics['metrics/mAP50(B)']:.4f}")
            if 'min_map50' in metrics and 'min_map50_epoch' in metrics:
                print(f"  min mAP50: {metrics['min_map50']:.4f} à l'epoch {metrics['min_map50_epoch']}")
        else:
            print(f"  ❌ Échec: {metrics.get('error', 'Erreur inconnue')}")
            
        print("-" * 40)
    
    print("\n📊 Une heatmap Seaborn avec mAP50 min et epochs correspondants a été générée dans le fichier '3fruits/heatmaps/min_map50_seaborn_heatmap.png'")

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()