from cv_utils.engine import train_one_epoch, evaluate
from cv_utils import utils
import argparse
import cv_utils.transforms as T
from cv_utils import CircuitsDataset
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
import torch, os

# CLI Parser
parser = argparse.ArgumentParser(description="CNN Trainer")
parser.add_argument("--seed", "-s", help="Set seed", type=int, default=22)
parser.add_argument("--val", "-v", help="Validation Size", type=int, default=2000)
parser.add_argument("--batch", "-b", help="Batch Size", type=int, default=16)
parser.add_argument("--lr", help="Learning Rate", type=float, default=0.005)
parser.add_argument("--epochs", "-e", help="Num Epochs", type=int, default=10)
parser.add_argument(
    "--checkpoint",
    "-c",
    help="Resume Training from Checkpoint",
    type=bool,
    default=False,
)
parser.add_argument("--ckp", help="Checkpoint path", type=str, required=True)
parser.add_argument(
    "--train", "-t", help="Size of training data", type=int, default=8000
)
parser.add_argument("--verb", help="print freq", type=int, default=10)
args = parser.parse_args()

# Add Transforms
def get_transform(train):
    if not train:
        transforms = [T.ToTensor()]
    else:
        transforms = [
            T.ToTensor(),
            T.RandomHorizontalFlip(0.5),
            T.GaussianNoise(),
            T.RandomRotate(angle=45),
        ]
    return T.Compose(transforms)


# DataLoader
dataset = CircuitsDataset(transforms=get_transform(train=True))
dataset_test = CircuitsDataset(transforms=get_transform(train=False))
torch.manual_seed(args.seed)
indices = torch.randperm(min(args.train + args.val, len(dataset))).tolist()
dataset = torch.utils.data.Subset(dataset, indices[: -args.val])
dataset_test = torch.utils.data.Subset(dataset_test, indices[-args.val :])
data_loader = torch.utils.data.DataLoader(
    dataset,
    batch_size=args.batch,
    shuffle=True,
    num_workers=4,
    collate_fn=utils.collate_fn,
)
data_loader_test = torch.utils.data.DataLoader(
    dataset_test,
    batch_size=args.batch,
    shuffle=False,
    num_workers=4,
    collate_fn=utils.collate_fn,
)
print(
    "We have: {} examples, {} are training and {} testing".format(
        len(indices), len(dataset), len(dataset_test)
    )
)

# Check CUDA
print("Is CUDA available", torch.cuda.is_available())
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

# Init Model
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
in_features = model.roi_heads.box_predictor.cls_score.in_features
model.roi_heads.box_predictor = FastRCNNPredictor(
    in_features, dataset.dataset.num_classes
)
model.to(device)

# Trainer
params = [p for p in model.parameters() if p.requires_grad]
optimizer = torch.optim.SGD(params, lr=args.lr, momentum=0.9, weight_decay=0.0005)
lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=3, gamma=0.95)

# if Checkpoint
if args.checkpoint:
    weights = sorted([file for file in os.listdir() if ".pt" in file])
    assert len(weights) > 0, "No weigths found"
    checkpoint = torch.load(os.path.join(args.ckp, weights[-1]))
    model.load_state_dict(checkpoint["model_state_dict"])
    optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
    num_epoch = checkpoint["epoch"]

# Training Loop
for epoch in range(args.epochs):
    train_one_epoch(model, optimizer, data_loader, device, epoch, print_freq=args.verb)
    lr_scheduler.step()
    evaluate(model, data_loader_test, device=device)
    torch.save(
        {
            "epoch": epoch + 1,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
        },
        os.path.join(args.ckp, f"model_ckp{epoch+1}.pth"),
    )
