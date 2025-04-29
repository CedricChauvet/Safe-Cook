"""
Tentative yolo L sur derniere base de données
"""

from ultralytics import YOLO
import torch
import cv2
import os
import glob
import multiprocessing
from torch.utils.tensorboard import SummaryWriter  # 🔥 ajout pour TensorBoard
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
            if isinstance(value, (int, float)):
                self.writer.add_scalar(f"YOLO/{key}", value, epoch)
def main():
    # Configuration du device
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    
    # TensorBoard Writer (log dans runs/yolo_train)
    writer = SummaryWriter("runs/yolo_train/passe5/exp1")  # 🔥

    # Chargement du modèle
    model = YOLO('yolo11l.pt').to(device)
    
    # Ajouter le callback TensorBoard
    tb_logger = TBLoggerCallback(writer)
    model.add_callback("on_fit_epoch_end", tb_logger.on_fit_epoch_end)  # 🔥

    # Configuration de l'entraînement avec les augmentations spécifiées
    hparams = dict(
            data='C:/Users/chauv/Desktop/bdd_3fruits/passe5/conf.yml',
            epochs=3,
            imgsz=640,
            batch=16,
            device=device,
            show=True,
            mosaic=1.0,
            mixup=0.0,
            copy_paste=0.0,
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
            name='valid3fruit'
        )

    # === Entraînement ===
    results = model.train(**hparams)

    # 🔥 Logging final des hyperparams + métriques YOLO
    metrics = results.metrics if hasattr(results, "metrics") else {}

    metrics_dict = {
        f"hparam/{k}": float(v)
        for k, v in metrics.items()
        if isinstance(v, (int, float))
    }

    writer.add_hparams(hparams, metrics_dict)
    print("📈 Résultats de l'entraînement :", results.metrics)
    writer.close()  # 🔥 Fermeture propre

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
