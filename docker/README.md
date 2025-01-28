# Readme
Notre projet consiste à envoyer des photos sur un serveur. Elles sont analysées avec un modele yolo. Ensuite le serveur renvoie au client les objets détéctés sur la photo.
Cela permet de gagner en performance lors de la détection et de récupérer les photos des usagers afin de garder une amélioration continue du modèle.

## partie conteneurisation du modele Yolo
 *  dockerfile <br />
 *  client.py <br />
 *  flask_server.py <br />
 *  ./images/ for testing. <br />
 *  ./mount/ for datas storage. <br />



#### Ceci est notre image, pytorch est indispensable pour utiliser Yolo.
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

### creation du conteneur
 
 Créer un repertoire de stockage en bind mount, -it permet de voir les print coté serveur.








### Create image
      docker build -t  docker_safecook . <br />

### Run the container 
      docker run -it -p 5000:5000 -v ${PWD}/mount:/mount --name sc_v2 docker_safecook


#### les images envoyées au serveur seront enregistrées dans le repertoire ./mount de windows.
#### pour verifier ce que contient le volume coté docker: docker exec -it sc_v2 ls /mount

