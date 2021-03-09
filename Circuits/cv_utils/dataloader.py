import os
import numpy as np
import torch
from PIL import Image
import json


class CircuitsDataset(object):
    def __init__(self, transforms=None):
        self.transforms = transforms
        self.imgs = [
            im
            for im in list(sorted(os.listdir(os.path.join("Data", "Images"))))
            if ".png" in im
        ]
        self.annots = [
            annot
            for annot in list(sorted(os.listdir(os.path.join("Data", "Annotations"))))
            if ".json" in annot
        ]
        self.label_encoder = {
            "background": 0,
            "battery": 1,
            "capacitor": 2,
            "resistor": 3,
            "inductor": 4,
            "diode": 5,
        }
        self.num_classes = len(self.label_encoder)

    def __getitem__(self, idx):
        img_path = os.path.join("Data", "Images", self.imgs[idx])
        annot_path = os.path.join("Data", "Annotations", self.annots[idx])
        img = Image.open(img_path).convert("L")
        annots = json.load(open(annot_path))["boxes"]
        boxes, labels = [], []
        for box, label in annots:
            x1, y1, x2, y2 = box
            boxes.append([min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)])
            labels.append(self.label_encoder[label])
        iscrowd = torch.zeros((len(boxes),), dtype=torch.int64)
        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        labels = torch.LongTensor(labels)
        image_id = torch.tensor([idx])
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    def __len__(self):
        return len(self.imgs)
