import pickle
import time

import torch
from PIL import Image

from sklearn.model_selection import KFold
from torch import nn, optim
from torch.utils.data import SubsetRandomSampler
from torchvision import datasets, models, transforms

from src.scores import *


def load_data():
    training_transforms = transforms.Compose(
        [
            transforms.Resize((224, 224), Image.LANCZOS),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )

    total_set = datasets.ImageFolder("data/DIBaS", transform=training_transforms)
    splits = KFold(n_splits=10, shuffle=True, random_state=42)
    return total_set, splits



def create_optimizer(model):
    params_to_update = model.parameters()

    n_params = 0
    for param in model.parameters():
        if param.requires_grad == True:
            n_params += 1

    criterion = nn.CrossEntropyLoss()

    optimizer = optim.Adam(params_to_update, lr=0.001, weight_decay=0.000004)
    
    device = get_device()
    criterion = criterion.to(device)
    model = model.to(device)

    return criterion, model, optimizer


def get_device():
    return "cpu"
    if torch.cuda.is_available():
        return "cuda"
    else:
        return "cpu"


def load_model_pretrained():
    model = models.shufflenet_v2_x1_0(pretrained=True)

    # fine tuning
    model.fc = nn.Linear(in_features=1024, out_features=32)
    
    return model


def main():
    batch_size = 32
    h_epochs = 10

    total_set, splits = load_data()
    train_labels = {value: key for (key, value) in total_set.class_to_idx.items()}
    with open("model_labels.pkl", "wb") as file:
        pickle.dump(train_labels, file)


    train_acc = []
    test_top1_acc = []
    test_top5_acc = []
    test_precision = []
    test_recall = []
    test_f1 = []
    times = []

    for fold, (train_idx, valid_idx) in enumerate(splits.split(total_set)):
        start_time = time.time()

        print("Fold : {}".format(fold))

        train_sampler = SubsetRandomSampler(train_idx)
        print("Samples in training:", len(train_sampler))
        valid_sampler = SubsetRandomSampler(valid_idx)
        print("Samples in test:", len(valid_sampler))

        # Train and val loaders
        train_loader = torch.utils.data.DataLoader(
            total_set, batch_size=batch_size, sampler=train_sampler
        )
        valid_loader = torch.utils.data.DataLoader(
            total_set, batch_size=1, sampler=valid_sampler
        )

        device = get_device()
        print("Pytorch Device:", device)

        criterion, model, optimizer = create_optimizer(load_model_pretrained())

        # Training
        for epoch in range(h_epochs):
            model.train()
            running_loss = 0.0
            running_corrects = 0
            trunning_corrects = 0

            for inputs, labels in train_loader:
                inputs = inputs.to(device)
                labels = labels.to(device)
                optimizer.zero_grad()

                with torch.set_grad_enabled(True):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)
                    loss.backward()
                    optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += (preds == labels).sum()
                trunning_corrects += preds.size(0)

            epoch_loss = running_loss / trunning_corrects
            epoch_acc = (running_corrects.double() * 100) / trunning_corrects
            train_acc.append(epoch_acc.item())

            print(
                "\t\t Training: Epoch({}) - Loss: {:.4f}, Acc: {:.4f}".format(
                    epoch, epoch_loss, epoch_acc
                )
            )

            # Validation
            model.eval()

            vrunning_loss = 0.0
            vrunning_corrects = 0
            num_samples = 0

            for data, labels in valid_loader:
                data = data.to(device)
                labels = labels.to(device)
                optimizer.zero_grad()

                with torch.no_grad():
                    outputs = model(data)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                vrunning_loss += loss.item() * data.size(0)
                vrunning_corrects += (preds == labels).sum()
                num_samples += preds.size(0)

            vepoch_loss = vrunning_loss / num_samples
            vepoch_acc = (vrunning_corrects.double() * 100) / num_samples

            print(
                "\t\t Validation({}) - Loss: {:.4f}, Acc: {:.4f}".format(
                    epoch, vepoch_loss, vepoch_acc
                )
            )

            model.class_to_idx = total_set.class_to_idx
            scores = get_scores(model, valid_loader)

            test_top1_acc.append(scores[0])
            test_top5_acc.append(scores[1])
            test_precision.append(scores[2])
            test_recall.append(scores[3])
            test_f1.append(scores[4])

            time_fold = time.time() - start_time
            times.append(time_fold)
            print("Total time per fold: %s seconds." % (time_fold))

        with open("model.pkl", "wb") as file:
            pickle.dump(model, file)

        break


if __name__ == "__main__":
    main()
