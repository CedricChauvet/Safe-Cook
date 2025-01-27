import os
import pandas as pd
make_df = __import__('0-explore_db').make_df
from torch.utils.data import Dataset
import torch
from PIL import Image

#IMAGE DATASET
class ImageDataset(Dataset):
    def __init__(self, dataframe, root_dir, transform=None):
        self.dataframe = dataframe
        self.root_dir = root_dir
        self.transform = transform
        self.label_to_int = None

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        row = self.dataframe.iloc[idx]
        img_name = os.path.join(self.root_dir, row['variety_image_path'])
        
        # Check if the file exists
        if not os.path.exists(img_name):
            raise FileNotFoundError(f"Image not found at path: {img_name}")

        # Load image and handle errors
        try:
            image = Image.open(img_name).convert('RGB')
        except Exception as e:
            raise ValueError(f"Error loading image at {img_name}: {e}")

        label = self.label_to_int[row['species']]
        amount = row['amount']  # Extract the amount value
        return image, label, amount, img_name


def make_dataset():
    train_df, test_df, label_int = make_df()        
    ma_data_train = ImageDataset(train_df, './archive/train/train/')
    test_data = ImageDataset(test_df, './archive/test/test/')
    dataset_size = len(ma_data_train)
    train_size = int(0.8 * dataset_size)
    val_size = dataset_size - train_size
    train_data, val_data = torch.utils.data.random_split(ma_data_train, [train_size, val_size])
    ma_data_train.label_to_int = label_int 
    return train_data, val_data, test_data




train_df, test_df, label_int = make_df()        
ma_data_train = ImageDataset(train_df, './archive/train/train/')

# penser a faire le test avec le dataset de test
test_data = ImageDataset(test_df, './archive/test/test/')

dataset_size = len(ma_data_train)
train_size = int(0.8 * dataset_size)
val_size = dataset_size - train_size

train_data, val_data = torch.utils.data.random_split(ma_data_train, [train_size, val_size])
ma_data_train.label_to_int = label_int 

# print("mes data", len(test_data), len(train_data), len(val_data)) # ok
# print("total", len(test_data) + len(train_data) + len(val_data)) # ok
print("tget", train_data[3]) # donne l'image et la classe int