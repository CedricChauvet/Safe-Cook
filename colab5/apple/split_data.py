import os
import shutil
import random
import argparse

def move_random_files(source_dir="train", valid_ratio=0.1, seed=42):
    """
    Déplace un pourcentage aléatoire de fichiers du répertoire ./source_dir/ vers ../valid/
    
    Args:
        source_dir (str): Répertoire source contenant les images et étiquettes (par défaut: "train")
        valid_ratio (float): Pourcentage de fichiers à déplacer vers valid (0.1 = 10%)
        seed (int): Graine pour la reproductibilité
    """
    random.seed(seed)
    print("running")
    # Chemins source (dans ./banana/train/)
    current_dir = os.path.abspath('.')
    source_images_dir = os.path.join(current_dir, source_dir, "images")
    source_labels_dir = os.path.join(current_dir, source_dir, "labels")
    
 

    # Chemins cible (dans ./banana/valid/)
    valid_dir = os.path.join(current_dir, "valid")
    valid_images_dir = os.path.join(valid_dir, "images")
    valid_labels_dir = os.path.join(valid_dir, "labels")
    
    
    # Vérification de l'existence des répertoires source
    if not os.path.exists(source_images_dir) or not os.path.exists(source_labels_dir):
        print(f"Erreur: Les répertoires images ou labels sont introuvables dans {source_dir}")
        return
    
    
    # Liste des fichiers d'images
    image_files = [f for f in os.listdir(source_images_dir)]
    
    # Nombre de fichiers à déplacer
    num_to_move = int(len(image_files) * valid_ratio)
    
    # Sélection aléatoire des fichiers à déplacer
    files_to_move = random.sample(image_files, num_to_move)
    
    print(f"Total de fichiers dans {source_images_dir}: {len(image_files)}")
    print(f"Déplacement de {num_to_move} fichiers ({valid_ratio*100:.1f}%) vers {valid_dir}")
    
    # Déplacement des fichiers
    moved_count = 0
    for img_file in files_to_move:
        base_name = os.path.splitext(img_file)[0]
        print(f"Moving {img_file} from {source_dir} to {valid_dir}")
        # Déplacer l'image
        src_img = os.path.join(source_images_dir, img_file)
        dst_img = os.path.join(valid_images_dir, img_file)
        shutil.move(src_img, dst_img)
        
        # Déplacer l'étiquette correspondante si elle existe
        label_file = base_name + '.txt'
        src_label = os.path.join(source_labels_dir, label_file)
        if os.path.exists(src_label):
            dst_label = os.path.join(valid_labels_dir, label_file)
            shutil.move(src_label, dst_label)
            moved_count += 1
        else:
            print(f"Attention: Étiquette manquante pour {img_file}")
    
    print(f"Réorganisation terminée. {moved_count} paires image/étiquette déplacées vers {valid_dir}")


move_random_files("train", 0.1, 42)