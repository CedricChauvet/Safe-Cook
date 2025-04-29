import random
import os
import sys
import shutil

fruit = sys.argv[1].lower()
number = sys.argv[2].lower()

cwd = os.getcwd()

print(f"Répertoire courant: {cwd}")

# Vérification des chemins source
source_labels_path = os.path.join(cwd, fruit, 'train', 'labels')
source_images_path = os.path.join(cwd, fruit, 'train', 'images')

print(f"Chemin des labels source: {source_labels_path}")
print(f"Chemin des images source: {source_images_path}")

# Vérification si les dossiers source existent
if not os.path.exists(source_labels_path):
    print(f"ERREUR: Le dossier source des labels n'existe pas: {source_labels_path}")
    sys.exit(1)
if not os.path.exists(source_images_path):
    print(f"ERREUR: Le dossier source des images n'existe pas: {source_images_path}")
    sys.exit(1)

# Création des dossiers de destination s'ils n'existent pas
dest_labels_path = os.path.join(cwd, fruit, f'{number}_instances', 'labels')
dest_images_path = os.path.join(cwd, fruit, f'{number}_instances', 'images')

print(f"Chemin des labels destination: {dest_labels_path}")
print(f"Chemin des images destination: {dest_images_path}")

os.makedirs(dest_labels_path, exist_ok=True)
os.makedirs(dest_images_path, exist_ok=True)

# Récupération de la liste des fichiers
file_list = os.listdir(source_labels_path)
print(f"Nombre de fichiers labels disponibles: {len(file_list)}")

i = 0  # compteur d'instances
j = 0  # compteur de fichiers
processed_files = set()  # Ensemble pour stocker les fichiers déjà traités

while i < int(number):
    # Sélectionnez un fichier non encore traité
    remaining_files = [f for f in file_list if f not in processed_files]
    
    # Si tous les fichiers ont été utilisés mais le nombre n'est pas atteint
    if not remaining_files:
        print("Attention: Tous les fichiers disponibles ont été utilisés.")
        break
        
    random_file = random.choice(remaining_files)
    processed_files.add(random_file)

    random_file_path = os.path.join(source_labels_path, random_file)

    random_file_png = random_file.replace('.txt', '.jpg')
    random_file_png_path = os.path.join(source_images_path, random_file_png)

    # Vérifier que les fichiers source existent
    if not os.path.exists(random_file_path):
        print(f"Fichier label non trouvé: {random_file_path}")
        continue
    if not os.path.exists(random_file_png_path):
        print(f"Fichier image non trouvé: {random_file_png_path}")
        continue

    # Copier les fichiers
    print(f"Copie de {random_file} et {random_file_png}")
    shutil.copy(random_file_path, os.path.join(dest_labels_path, random_file))
    shutil.copy(random_file_png_path, os.path.join(dest_images_path, random_file_png))
    
    # Compte le nombre d'instances dans le fichier
    with open(random_file_path, "r") as fichier:
        liste_lignes = fichier.readlines()
        i += len(liste_lignes)
        j += 1

print("Nombre d'instances:", i)
print("Nombre de fichiers:", j)