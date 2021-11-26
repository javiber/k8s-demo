import os
from pathlib import Path

import click
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.models as models
import torchvision.transforms as transforms
from tqdm import tqdm

transform = transforms.Compose(
    [
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,)),  # mean and std of mnist
    ]
)
# store data in the configured cahe which should be a volume
cache_path = Path(os.environ["CACHE_PATH"])


@click.command()
@click.option("--epochs", "-e", default=3, type=int, help="Number of epochs to run.")
@click.option("--batch-size", "-b", default=2048, type=int, help="Training batch size.")
@click.option("--num-workers", "-w", default=16, type=int, help="workers to load data.")
@click.option(
    "--learning-rate", "-lr", default=0.001, type=float, help="learning rate for SGD"
)
@click.option("--momentum", "-m", default=0.9, type=float, help="momentum for SGD")
def train(epochs, batch_size, num_workers, learning_rate, momentum):
    train_set = torchvision.datasets.MNIST(
        root=cache_path / "data", train=True, download=True, transform=transform
    )
    train_loader = torch.utils.data.DataLoader(
        train_set, batch_size=batch_size, shuffle=True, num_workers=num_workers
    )

    test_set = torchvision.datasets.MNIST(
        root=cache_path / "data", train=False, download=True, transform=transform
    )
    test_loader = torch.utils.data.DataLoader(
        test_set, batch_size=batch_size, shuffle=False, num_workers=num_workers
    )
    model = models.resnet18(pretrained=False, num_classes=10)
    # for mnist we hace a sinle input channel, the rest should be the same as resnet18
    # TODO: get the values from the model.conv1 before overwiting it
    model.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=learning_rate, momentum=momentum)

    trainer = Trainer(
        epochs=epochs,
        train_loader=train_loader,
        test_loader=test_loader,
        model=model,
        optimizer=optimizer,
        criterion=criterion,
        device=torch.device("cuda"),
    )
    trainer.run()

    print("Finished Training")


class Trainer:
    def __init__(
        self,
        epochs,
        train_loader,
        test_loader,
        model,
        optimizer,
        criterion,
        device,
    ) -> None:
        self.epochs = epochs
        self.device = device
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.model = model
        self.model.to(self.device)
        self.optimizer = optimizer
        self.criterion = criterion

    def run(self):
        self.test()

        for epoch in range(self.epochs):
            self.train_epoch(epoch)
            self.test(epoch)

    def test(self, epoch=-1):
        self.model.eval()
        test_loss = 0
        correct = 0
        with torch.no_grad():
            for (inputs, labels) in self._dl_progres(self.test_loader, desc="test"):
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                output = self.model(inputs)
                test_loss += self.criterion(output, labels).item()  # sum up batch loss
                pred = output.argmax(
                    dim=1, keepdim=True
                )  # get the index of the max log-probability
                correct += pred.eq(labels.view_as(pred)).sum().item()

        test_loss /= len(self.test_loader.dataset)
        accuracy = correct / len(self.test_loader.dataset)

        print(
            f"TEST after epoc {epoch}: Average loss: {test_loss:.4f}, Accuracy: {100.0 * accuracy:.0f}%)\n"
        )

    def _dl_progres(self, data_loader, desc):
        return tqdm(
            data_loader,
            total=len(data_loader),
            desc=desc,
            leave=True,
        )

    def train_epoch(self, epoch):
        self.model.train()

        for i, (inputs, labels) in enumerate(
            self._dl_progres(self.train_loader, desc=f"epoc {epoch}")
        ):
            inputs, labels = inputs.to(self.device), labels.to(self.device)

            # zero the parameter gradients
            self.optimizer.zero_grad()

            # forward + backward + optimize
            outputs = self.model(inputs)
            loss = self.criterion(outputs, labels)
            loss.backward()
            self.optimizer.step()


if __name__ == "__main__":
    train()
