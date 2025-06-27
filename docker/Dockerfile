# Use the official PyTorch image with CUDA support
FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    wget \
    libgl1-mesa-glx \
    libglib2.0-0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy application files to the working directory
COPY server.py 3mentors.pt ./

# Install Python dependencies
RUN pip install --no-cache-dir \
    flask \
    opencv-python-headless \
    numpy==1.24.1 \
    requests \
    torch \
    torchvision \
    ultralytics \
    pymongo

# Expose the port used by the Flask application
EXPOSE 5000

# Define the default command to run the server
CMD ["python", "server.py"]

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
# COPY yolo11L-seg60.pt yolo11L-seg60.pt
COPY 3mentors.pt /app/3mentors.pt
EXPOSE 5000

CMD ["python", "/app/flask_server.py"]