this is the README


### création de l'image
 docker build -t  docker_safecook .

 ### creation du conteneur
 
 Créer un repertoire de stockage en bind mount, -it permet de voir les print coté serveur
 
 docker run -it -p 5000:5000 -v ${PWD}/mount:/mount --name sc_v2 docker_safecook
#### les images envoyées au serveur seront enregistrées dans le repertoire ./mount de windows
#### pour verifier ce que contient le volume:

 docker exec -it sc_v2 ls /mount

