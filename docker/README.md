this is the README


# création de l'image
 docker build -t  docker_safecook .
 
 //créer un repertoire de stockage en bind mount, -it permet de voir les print coté serveur
 
 docker run -it -p 5000:5000 -v ${PWD}/mount:/mount --name sc_v3 docker_safecook



//pour verifier ce que contient le volume:

 docker exec -it ced ls /mount

