import os
import yaml
from PIL import Image
import numpy as np
from pathlib import Path
from typing import Literal

class LVISDataset:
    def __init__(self, root_dir: str, split: Literal['train', 'val', 'test'] = 'train'):
        """
        Initialise le dataset LVIS avec labels format YOLO txt
        
        Args:
            root_dir (str): Chemin vers le dossier racine contenant images/, labels/ et data.yaml
            split (str): Partition à utiliser ('train', 'val', ou 'test')
        """
        self.root_dir = Path(root_dir)
        self.split = split
        self.images_dir = self.root_dir / 'images' / split
        self.labels_dir = self.root_dir / 'labels' / split
        
        # Chargement du fichier data.yaml
        with open(self.root_dir / 'data.yaml', 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
            
        # Vérification de la structure du dataset
        self._validate_directory_structure()
        
        # Liste des images avec plusieurs extensions possibles
        self.image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif']:
            self.image_files.extend(list(self.images_dir.glob(ext)))
        self.image_files = sorted(self.image_files)
        
        if not self.image_files:
            print(f"Attention: Aucune image trouvée dans {self.images_dir}")
            print(f"Contenu du dossier: {list(self.images_dir.iterdir())}")
            
        # Liste des labels (fichiers txt)
        self.label_files = []
        for img_path in self.image_files:
            # Remplace l'extension de l'image par .txt et change le dossier images en labels
            label_path = self.labels_dir / f"{img_path.stem}.txt"
            self.label_files.append(label_path)
        
        missing_labels = [f for f in self.label_files if not f.exists()]
        if missing_labels:
            print(f"Attention: {len(missing_labels)} fichiers labels manquants")
            
        print(f"Dataset {split} chargé:")
        print(f"- {len(self.image_files)} images")
        print(f"- {len([f for f in self.label_files if f.exists()])} fichiers labels")

    def _validate_directory_structure(self):
        """Vérifie que la structure du dataset est correcte"""
        assert self.images_dir.exists(), f"Le dossier images/{self.split} n'existe pas: {self.images_dir}"
        assert self.labels_dir.exists(), f"Le dossier labels/{self.split} n'existe pas: {self.labels_dir}"

    def _read_label_file(self, label_path):
        """
        Lit un fichier label au format YOLO txt
        Format: class x_center y_center width height
        Toutes les valeurs sont normalisées entre 0 et 1
        """
        boxes = []
        if label_path.exists():
            with open(label_path, 'r') as f:
                for line in f:
                    data = line.strip().split()
                    if len(data) == 5:
                        class_id = int(data[0])
                        x_center, y_center = float(data[1]), float(data[2])
                        width, height = float(data[3]), float(data[4])
                        boxes.append({
                            'class_id': class_id,
                            'x_center': x_center,
                            'y_center': y_center,
                            'width': width,
                            'height': height
                        })
        return boxes
        
    def __len__(self):
        """Retourne le nombre d'images dans le dataset"""
        return len(self.image_files)
    
    def __getitem__(self, idx):
        """
        Charge une image et ses annotations
        
        Args:
            idx (int): Index de l'image à charger
            
        Returns:
            dict: Dictionnaire contenant l'image et ses annotations
        """
        # Chargement de l'image
        image_path = self.image_files[idx]
        image = Image.open(image_path)
        
        # Chargement des annotations
        label_path = self.label_files[idx]
        boxes = self._read_label_file(label_path)
            
        return {
            'image': image,
            'boxes': boxes,
            'image_path': str(image_path),
            'label_path': str(label_path)
        }
    
    def get_classes(self):
        """Retourne la liste des classes depuis data.yaml"""
        return self.config.get('names', [])

# Exemple d'utilisation
if __name__ == "__main__":
    # Création du dataset
    dataset = LVISDataset("C:/Users/chauv/Desktop/Safe-Cook/bdd_aliments_yolo/LVIS_fruit_vegetables", split='train')
    
    print(f"\nClasses disponibles: {dataset.get_classes()}")
    
    # Exemple de chargement d'une image
    if len(dataset) > 0:
        sample = dataset[1]
        print(f"\nPremière image:")
        print(f"Dimensions: {sample['image'].size}")
        print(f"Nombre de boxes: {len(sample['boxes'])}")
        if sample['boxes']:
            print("Première box:", sample['boxes'][0])