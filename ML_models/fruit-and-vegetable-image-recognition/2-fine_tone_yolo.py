from ultralytics import YOLO
import torch
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
make_dataset = __import__('1-create-dataset').make_dataset
class YOLOTrainer:
    def __init__(self, model_path='../yolo_pt/yolo11l.pt'):
        self.model = YOLO(model_path)
        
        # Définition des transformations pour redimensionner à 640x640
        self.transform = transforms.Compose([
            transforms.Resize((640, 640)),  # Redimensionne à 640x640
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                              std=[0.229, 0.224, 0.225])
        ])

    def train(self, train_dataset, val_dataset, test_dataset, epochs=100):
        """
        Fine-tune YOLO avec des datasets retournant (PIL Image, int label)
        Les images seront redimensionnées à 640x640
        """
        train_loader = DataLoader(
            train_dataset,
            batch_size=16,
            shuffle=True,
            num_workers=8,
            pin_memory=True,
            collate_fn=self.collate_fn
        )
        
        val_loader = DataLoader(
            val_dataset,
            batch_size=16,
            shuffle=False,
            num_workers=8,
            pin_memory=True,
            collate_fn=self.collate_fn
        )
        
        training_args = {
            'data': None,
            'epochs': epochs,
            'imgsz': 640,  # Taille d'image fixée à 640
            'device': 'cuda' if torch.cuda.is_available() else 'cpu',
            'patience': 50,
            'save': True,
            'name': 'yolov11_640x640'
        }
        
        self.model.train_loader = train_loader
        self.model.val_loader = val_loader
        
        results = self.model.train(**training_args)
        return results, self.model
    
    def collate_fn(self, batch):
        """
        Convertit les images PIL en tensors 640x640
        """
        images, labels = zip(*batch)
        
        # Conversion des images PIL en tensors 640x640
        transformed_images = torch.stack([self.transform(img) for img in images])
        
        # Conversion des labels
        transformed_labels = []
        for label in labels:
            yolo_label = torch.tensor([
                [float(label), 0.5, 0.5, 1.0, 1.0]
            ])
            transformed_labels.append(yolo_label)
        
        transformed_labels = torch.stack(transformed_labels)
        print(transformed_images.shape, transformed_labels.shape)
        return transformed_images, transformed_labels

# Utilisation simple
def train_yolo(train_dataset, val_dataset, test_dataset, epochs=100):
    trainer = YOLOTrainer()
    results, model = trainer.train(train_dataset, val_dataset, test_dataset, epochs=epochs)
    return results, model

train_data, val_data, test_data = make_dataset() #voir 1-create_dataset.py
results, model = train_yolo(train_data, val_data, test_data, epochs=100)