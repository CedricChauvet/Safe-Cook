FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    git \
    wget \
    libgl1-mesa-glx \
    libglib2.0-0

# Installer les dépendances Python
RUN pip install --no-cache-dir \
    flask \
    opencv-python-headless \
    numpy==1.24.1\
    requests \
    torch \
    torchvision \
    ultralytics \
    pymongo

# Copier le script serveur
COPY flask_server.py /app/flask_server.py

EXPOSE 5000

CMD ["python", "/app/flask_server.py"]