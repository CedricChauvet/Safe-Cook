import glob
import os
import numpy as np
import matplotlib.pyplot as plt


def main():

    names = {
    0: "amande",
    1: "pomme",
    2: "abricot",
    3: "artichaut",
    4: "asperge",
    5: "avocat",
    6: "banane",
    7: "tofu",
    8: "poivron",
    9: "mûre",
    10: "myrtille",
    11: "brocoli",
    12: "choux de Bruxelles",
    13: "cantaloup",
    14: "carotte",
    15: "chou-fleur",
    16: "piment de Cayenne",
    17: "céleri",
    18: "cerise",
    19: "pois chiche",
    20: "piment",
    21: "clémentine",
    22: "noix de coco",
    23: "maïs",
    24: "concombre",
    25: "datte",
    26: "aubergine",
    27: "figue",
    28: "ail",
    29: "gingembre",
    30: "fraise",
    31: "courge",
    32: "raisin",
    33: "haricot vert",
    34: "oignon vert/ciboule",
    35: "tomate",
    36: "kiwi",
    37: "citron",
    38: "laitue",
    39: "citron vert",
    40: "mandarine",
    41: "melon",
    42: "champignon",
    43: "oignon",
    44: "orange",
    45: "papaye",
    46: "petit pois",
    47: "pêche",
    48: "poire",
    49: "kaki",
    50: "cornichon",
    51: "ananas",
    52: "pomme de terre",
    53: "prune",
    54: "citrouille",
    55: "radis",
    56: "framboise",
    57: "fraise",
    58: "patate douce",
    59: "tomate",
    60: "navet",
    61: "pastèque",
    62: "courgette"
    }


    # Spécifiez le chemin du répertoire
    path = "C:/Users/chauv/Desktop/holberton-demoday/fine-tuning/fruit_vegetable/Fruits-And-Vegetables-Detection-Dataset/LVIS_Fruits_And_Vegetables/labels/train/train"

    # Utilisez glob pour trouver tous les fichiers .txt
    fichiers_txt = glob.glob(os.path.join(path, '*.txt'))
    liste_recettes = []
    detection = np.zeros((63))
    print(detection)
    for file in fichiers_txt:
        
        with open(file, 'r', encoding='utf-8') as f:
            lignes = f.readlines()
            for ligne in lignes:
                aliment = ligne.split(" ")[0]
                detection[int(aliment)] += 1

    # Trier de manière descendante avec les indices
    # ici on peut modifier le slice pour choisir le nombre d'aliments à afficher
    indices_tries = np.argsort(-detection)[:]  # Le - inverse l'ordre pour avoir descendant
    
    detection_triee = detection[indices_tries]



    # Pour afficher le résultat avec les noms
    for i, indice in enumerate(indices_tries):
        print(f"{names[indice]}: {detection_triee[i]} détections, a l'indice {indice}")

    labels_tries = [names[i] for i in indices_tries]  # Correspondant aux labels

    # Création du pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(
        detection_triee,
        labels=labels_tries,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 10}
    )

    # Ajouter un titre
    plt.title("Top 10 des détections triées", fontsize=14)

    # Afficher
    plt.tight_layout()
    plt.show()
    #print(detection)
if __name__ == "__main__":
    main()
