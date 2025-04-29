"""
change the number of a class in the dataset from 0 to n=1
Ca a marché sur les bananes, le numero de classe vaux bien 1
Attention a ne pas corrpompre les fichiers txt
"""

import numpy as np
import os
import sys

# Define the fruit to work with attention la majuscule
fruit = sys.argv[1].lower()
if fruit.lower() == 'apple': cls = 0
elif fruit.lower() == 'banana': cls = 1
elif fruit.lower() == 'orange': cls = 2
elif fruit.lower() == 'potatoe': cls = 3
elif fruit.lower() == 'salad': cls = 4
elif fruit.lower() == 'tomato': cls = 5


else :
    print("Fruit not found")
    exit()
print(f"fruit: {fruit} class: {cls}")
#adding a parameter to
# Define the path to the directory containing the images
data_dir_train = f'D:/00_DataBase_safecook/passe3/{fruit}/train/labels/'
data_dir_valid = f'D:/00_DataBase_safecook/passe3/{fruit}/valid/labels/'
obj = 0
for data_dir in [data_dir_train, data_dir_valid]:
    try:
        # liste des fichiers txt dans le répertoire data_dir
        files = os.listdir(data_dir)
        print(f"Nombre d'images", len(files))
        for file in files:
            # Load the contents of the file
            with open(os.path.join(data_dir, file), 'r') as f:
                content = f.readlines()
                obj+=len(content)
                # Modifier le contenu
            new_content = []
            for line in content:
                
                split_line = line.split() 
                # Modifier la classe 0 en classe 1
                split_line[0] = cls
                # Convertir la ligne modifiée en une chaîne de caractères
                new_line = ' '.join(map(str, split_line)) + '\n'
                new_content.append(new_line)
            
            # Écrire le contenu modifié dans le fichier
            with open(os.path.join(data_dir, file), 'w') as f:
                f.writelines(new_content)
    except:
        pass
        # print(f'No data in {data_dir}')
print(f"Nombre d'objets: {fruit} ", obj)  