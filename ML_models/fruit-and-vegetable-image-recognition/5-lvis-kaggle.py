

import os
from ultralytics import YOLO
import torch
import cv2
import matplotlib.pyplot as plt



model = YOLO('yolov9c.pt')



results = model.train(data='/home/cedrix/Bureau/holbertonschool-demoday/LVIS_Fruits_And_Vegetables/data.yaml', epochs=30, imgsz=640, batch=8, lr0=0.001)

model_path = "/pytorch_model.bin"
torch.save(model.model.state_dict(), model_path)  
if os.path.exists(model_path):
    print("Model weights saved successfully.")
else:
    print("Model weights were not saved. Check the path.")