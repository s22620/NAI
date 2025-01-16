"""
SIECI NEURONOWE - KLASYFIKACJA ZWIERZĄT

Autorzy: Jakub Marcinkowski s21021, Dagmara Gibas s22620

Opis problemu:
1. Wykorzystanie sieci neuronowych do rozpoznawania obrazów zwierząt z datasetu CIFAR-10.
2. Trenowanie modelu, analiza wyników i prezentacja macierzy pomyłek.

Instrukcja:
1. Upewnij się, że masz zainstalowany Python 3+ oraz narzędzie pip.
2. Zainstaluj wymagane biblioteki:
   pip install numpy
   pip install torch
   pip install torchvision
   pip install sklearn
   pip install matplotlib
3. Uruchom skrypt:
   python <Zadanie_2>.py

Framework: PyTorch
Zbiór danych: CIFAR-10
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

if __name__ == '__main__':


    # Ładowanie i przetwarzanie danych
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])
    batch_size = 4
    trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size, shuffle=True, num_workers=2)
    testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=2)
    classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')


    # Definicja sieci neuronowej
    class Net(nn.Module):
        def __init__(self):
            super().__init__()
            self.conv1 = nn.Conv2d(3, 6, 5)
            self.pool = nn.MaxPool2d(2, 2)
            self.conv2 = nn.Conv2d(6, 16, 5)
            self.fc1 = nn.Linear(16 * 5 * 5, 120)
            self.fc2 = nn.Linear(120, 84)
            self.fc3 = nn.Linear(84, 10)

        def forward(self, x):

            x = self.pool(F.relu(self.conv1(x)))
            x = self.pool(F.relu(self.conv2(x)))
            x = torch.flatten(x, 1)  # flatten all dimensions except batch
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            x = self.fc3(x)
            return x


    net = Net()

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

    # Trenowanie sieci
    for epoch in range(2):

        for i, data in enumerate(trainloader, 0):
            inputs, labels = data
            optimizer.zero_grad()
            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

    print('Finished Training')

    # Testowanie modelu
    dataiter = iter(testloader)
    images, labels = next(dataiter)
    outputs = net(images)
    _, predicted = torch.max(outputs, 1)

    correct = 0
    total = 0
    predicted_labels = []
    true_labels = []

    with torch.no_grad():
        for data in testloader:
            images, labels = data
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            predicted_labels.extend(predicted.tolist())
            true_labels.extend(labels.tolist())

    print("#" * 40)
    print("\nClassifier performance on test dataset\n")
    print(classification_report(true_labels, predicted_labels))
    print("#" * 40 + "\n")
# Ocena wyników
    cm = confusion_matrix(true_labels, predicted_labels, normalize='all')
    cmd = ConfusionMatrixDisplay(cm, display_labels=classes)
    fig, ax = plt.subplots(figsize=(10, 10))
    cmd.plot(ax=ax)
    plt.show()