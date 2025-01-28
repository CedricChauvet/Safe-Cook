# Readme
Our project consists of sending photos to a server. They are analyzed with a yolo model. Then the server returns to the client the objects detected on the photo. This allows to gain in performance during detection and to retrieve the photos of the users in order to keep a continuous improvement of the model.

## partie conteneurisation du modele Yolo
 *  dockerfile <br />
 *  client.py <br />
 *  flask_server.py <br />
 *  ./images/ for testing. <br />
 *  ./mount/ for datas storage. <br />



#### This is our image, pytorch is essential to use Yolo.
      FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

### creation du conteneur
 
 Créer un repertoire de stockage en bind mount, -it permet de voir les print coté serveur.








### Create image
      docker build -t  docker_safecook .

### Run the container 
      docker run -it -p 5000:5000 -v ${PWD}/mount:/mount --name sc_v2 docker_safecook


#### les images envoyées au serveur seront enregistrées dans le repertoire ./mount de windows.
#### pour verifier ce que contient le volume coté docker: docker exec -it sc_v2 ls /mount

