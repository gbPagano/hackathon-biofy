import pickle

from PIL import Image
from torchvision import transforms


def preprocess_image(img):
    transform = transforms.Compose(
        [
            transforms.Resize((224, 224), Image.LANCZOS),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )

    return transform(img).unsqueeze(0)


def get_model():
    with open("models/model.pkl", "rb") as pkl:
        model = pickle.load(pkl)

    return model


def get_labels():
    with open("models/model_labels.pkl", "rb") as pkl:
        labels = pickle.load(pkl)

    return labels
