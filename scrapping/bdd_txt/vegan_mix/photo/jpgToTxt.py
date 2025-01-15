
import os
import glob
import base64


# Spécifiez le chemin du répertoire
path = './'

# Utilisez glob pour trouver tous les fichiers .txt
fichiers_txt = glob.glob(os.path.join(path, '*.jpg'))
liste_recettes = [] 
for file in fichiers_txt:
    # Lire l'image JPG
    with open(file, 'rb') as image_file:
        # Convertir en base64
        encoded_string = base64.b64encode(image_file.read())
        
    # Enregistrer le base64 dans un fichier texte
    with open(f'{file[:-4]}.txt', 'wb') as txt_file:
        txt_file.write(encoded_string)