from pathlib import Path

import torch
from torch.utils.data import TensorDataset
from torchvision import transforms
from PIL import Image
import torch.nn.functional as F


import torch
import torchvision
import torch.nn as nn
from torch.utils.data import TensorDataset, Dataset, DataLoader, Subset, random_split
from sklearn.model_selection import train_test_split
from torchvision import transforms

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.utils import mapped_labels, mapped_labels_2
from PIL import Image, ImageFilter


def cortar_imagem(imagem, tamanho_corte_x, tamanho_corte_y):
    largura, altura = imagem.size
    cortes = []
    for y in range(0, altura, tamanho_corte_y):
        for x in range(0, largura, tamanho_corte_x):
            cortes.append(imagem.crop((x, y, x + tamanho_corte_x, y + tamanho_corte_y)))
    return cortes
 # Carregar a imagem
# imagem = Image.open("data/small/Bacteroides.fragilis/Bacteroides.fragilis_0001.jpg")

# # Definir o tamanho do corte desejado


# # Cortar a imagem em várias partes
# cortes = cortar_imagem(imagem, 256, 192)

# # Mostrar os cortes (exemplo para os primeiros 9 cortes)
# imagem.show()
# for i, corte in enumerate(cortes[:9]):
#     corte.show()


def preprocess_image(image_path, target_size):
    img = Image.open(image_path)  # colorul
    # img = Image.open(image_path).convert("L")  # black and white
    img = img.filter(ImageFilter.GaussianBlur(radius=2))
    # img = img.point(lambda p: 0 if p < 190 else 255)
    # img = img.filter(ImageFilter.FIND_EDGES)
    preprocess = transforms.Compose(
        [
            # transforms.Resize(target_size),
            transforms.ToTensor(),
        ]
    )
    cortes = cortar_imagem(img, 256, 192)
    res = []
    for c in cortes:
        img_tensor = preprocess(c)
        img_tensor = img_tensor.unsqueeze(0)
        
        res.append(img_tensor)
    # c.show()
    # input()
    return res
    # img_tensor = preprocess(img)
    # img_tensor = img_tensor.unsqueeze(0)
    # return [img_tensor]


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Pytorch Device:", device)


image_path = "data/small/Actinomyces.israeli/Actinomyces.israeli_0003.jpg"
target_size = (256, 192)
# target_size = (128, 96)

# input_image = preprocess_image(image_path, target_size).to(device)

train_data = []
train_labels = []
for sub_dir in Path("data/small").iterdir():
    for img in sub_dir.iterdir():
        label, *_ = img.name.split("_")
        # label, *_ = label.split(".")
        img_data = preprocess_image(img, target_size)
        for j, i in enumerate(img_data):
            if j < 3:
                # break
                train_data.append(i.to(device))
                train_labels.append(mapped_labels[label])
                # train_labels.append(mapped_labels_2[label])

        
x_train = torch.cat(train_data)
y_train = torch.tensor(train_labels)

dataset = TensorDataset(x_train, y_train)

a = int(x_train.shape[0] * 0.75)
b = x_train.shape[0] - a
training_set, validation_set = random_split(dataset, [a, b], generator=torch.Generator())


batch_size = 8
# torch.manual_seed(1)

train_dl = DataLoader(training_set, batch_size, shuffle=True)
valid_dl = DataLoader(validation_set, batch_size, shuffle=True)
