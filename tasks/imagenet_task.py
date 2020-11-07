import torch.utils.data as torch_data
import torchvision
from torchvision.transforms import transforms

from models.resnet import resnet18
from tasks.task import Task


class ImagenetTask(Task):

    def load_data(self):

        train_transform = transforms.Compose([
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            self.normalize,
        ])
        test_transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            self.normalize,
        ])

        self.train_dataset = torchvision.datasets.ImageNet(
            root=self.params.data_path,
            split='train', transform=train_transform)

        self.test_dataset = torchvision.datasets.ImageNet(
            root=self.params.data_path,
            split='val', transform=test_transform)

        self.train_loader = torch_data.DataLoader(self.train_dataset,
                                                  batch_size=self.params.batch_size,
                                                  shuffle=True, num_workers=2)
        self.test_loader = torch_data.DataLoader(self.test_dataset,
                                                 batch_size=self.params.test_batch_size,
                                                 shuffle=False, num_workers=2)

        with open(
                f'{self.params.data_path}/imagenet1000_clsidx_to_labels.txt') \
                as f:
            self.classes = eval(f.read())

    def build_model(self) -> None:
        self.model = resnet18(num_classes=len(self.classes))