from ultralytics import YOLO
import torch
device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
model = YOLO('yolov8l-seg.pt').to(device)




results = model.train(data='/home/cedrix/Bureau/holbertonschool-demoday/db_FruitsVegetables_2/archive/conf.yml', epochs=50, imgsz=640)
# model = YOLO('/kaggle/working/runs/segment/train2/weights/best.pt')