this is the README



 docker build -t  my-app .
 
 //créer un repertoire de stockage en bind mount
 
 docker run -p 5000:5000 -v ${PWD}/mount:/mount --name ced my-app

//pour verifier ce que contient le volume:
 docker exec -it ced ls /mount

