from ultralytics import YOLO
import torch
from matplotlib import pyplot as plt
device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
model = YOLO('/home/cedrix/Bureau/holbertonschool-demoday/db_FruitsVegetables_2/yolo_pt/best.pt').to(device)



img_path = '/home/cedrix/Bureau/holbertonschool-demoday/db_FruitsVegetables_2/archive/segmentation_test/segmentation_test/test/7491.jpg'
prediction = model(img_path)
annotated_frame = prediction[0].plot()
plt.imshow(annotated_frame)

plt.show()