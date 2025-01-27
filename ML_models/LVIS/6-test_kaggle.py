import matplotlib.pyplot as plt
from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt



model = YOLO("yolo_finetune.pt")
img_path = "images/test/20240326_3c8f4813-06ae-4d71-8dd3-d6f5d2e41c9a_1_png.rf.de9321530f6982f8a97c0b5965edaff0.jpg"
image = cv2.imread(img_path)
final = model(img_path) #The model is using the weights from your custom-trained model, not the generic pre-trained YOLO model.
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


for result in final:
    plt.imshow(cv2.cvtColor(result.plot(), cv2.COLOR_BGR2RGB))  # plot() draws bounding boxes on the image
    plt.axis("off")
    plt.show()