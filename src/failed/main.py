import torch
from torchvision import transforms
from PIL import Image


def preprocess_image(image_path, target_size):
    # img = Image.open(image_path)  # colorul
    img = Image.open(image_path).convert('L')  # black and white
    preprocess = transforms.Compose(
        [
            transforms.Resize(target_size),
            transforms.ToTensor(),
        ]
    )
    img_tensor = preprocess(img)
    img_tensor = img_tensor.unsqueeze(0)
    return img_tensor


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Pytorch Device:", device)

image_path = "data/small/Actinomyces.israeli/Actinomyces.israeli_0003.jpg"
target_size = (128, 128)

input_image = preprocess_image(image_path, target_size).to(device)
