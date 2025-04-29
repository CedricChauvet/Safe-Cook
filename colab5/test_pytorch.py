import torch
print(torch.cuda.is_available())  # Devrait afficher True
print(torch.cuda.get_device_name(0))  # Devrait afficher "NVIDIA GeForce RTX 4080"