import argparse
import os
from torchvision.transforms import functional as F
from PIL import Image, ImageDraw
import numpy as np
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
import torch
import torchvision


def predictBoxes(
    model,
    img_path,
    save_path,
    device,
    color_decoder={1: "blue", 2: "cyan", 3: "red", 4: "green"},
):
    filename = img_path.split("/")[-1]
    img = Image.open(img_path).convert("RGB")
    img.save(os.path.join(save_path, f"raw_{filename}"))
    imgt = F.to_tensor(img)
    out = model([imgt.to(device)])[0]
    draw = ImageDraw.Draw(img)
    for box, ele in zip(
        list(np.array(out["boxes"].cpu().detach())), list(np.array(out["labels"].cpu()))
    ):
        draw.rectangle(
            box, outline=color_decoder[ele], width=3,
        )
    img.save(os.path.join(save_path, f"box_{filename}"))


if __name__ == "__main__":
    # Check CUDA
    print("Is CUDA available", torch.cuda.is_available())
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    num_classes = 5

    # Init Model
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    model.to(device)

    # Load Weights
    weights = sorted([file for file in os.listdir() if ".pt" in file])
    assert len(weights) > 0, "No weigths found"
    checkpoint = torch.load(os.path.join(weights[-1]))
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
