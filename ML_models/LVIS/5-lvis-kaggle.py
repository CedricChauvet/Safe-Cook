

import os
from ultralytics import YOLO
import torch
import cv2
import matplotlib.pyplot as plt



model = YOLO('yolov9c.pt')



# results = model.train(data='/home/cedrix/Bureau/holbertonschool-demoday/LVIS_Fruits_And_Vegetables/data.yaml',
model.train(
   data='/home/cedrix/Bureau/holbertonschool-demoday/LVIS_Fruits_And_Vegetables/data.yaml',
   epochs=30,
   patience=100, 
   batch=8,
   imgsz=640,
   workers=8,
   save=True,
   save_period=-1,
   pretrained=True,
   optimizer='auto',
   lr0=0.001,
   lrf=0.01,
   momentum=0.937,
   weight_decay=0.0005,
   warmup_epochs=3.0,
   warmup_momentum=0.8,
   warmup_bias_lr=0.1,
   box=7.5,
   cls=0.5,
   dfl=1.5,
   pose=12.0,
   kobj=1.0,
   label_smoothing=0.0,
   amp=True,
   close_mosaic=10,
   hsv_h=0.015,
   hsv_s=0.7, 
   hsv_v=0.4,
   degrees=0.0,
   translate=0.1,
   scale=0.5,
   shear=0.0,
   perspective=0.0,
   flipud=0.0,
   fliplr=0.5,
   mosaic=1.0,
   mixup=0.0,
   copy_paste=0.0,
   auto_augment='randaugment',
   erasing=0.4,
   val=True,
   iou=0.7
)

model.save("yolo_finetune.pt")