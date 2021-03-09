import random
import torch
import numpy as np
from torchvision.transforms import functional as F
from cv_utils.bbox_util import *
from torchvision.transforms import ToPILImage
from PIL import Image


def _flip_coco_person_keypoints(kps, width):
    flip_inds = [0, 2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 12, 11, 14, 13, 16, 15]
    flipped_data = kps[:, flip_inds]
    flipped_data[..., 0] = width - flipped_data[..., 0]
    # Maintain COCO convention that if visibility == 0, then x, y = 0
    inds = flipped_data[..., 2] == 0
    flipped_data[inds] = 0
    return flipped_dataå


class Compose(object):
    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, image, target):
        for t in self.transforms:
            image, target = t(image, target)
        return image, target


class RandomVerticalFlip(object):
    def __init__(self, prob):
        self.prob = prob

    def __call__(self, image, target):
        if random.random() < self.prob:
            height, width = image.shape[-2:]
            image = image.flip(-1)
            bbox = target["boxes"]
            bbox[:, [3, 1]] = height - bbox[:, [3, 1]]
            target["boxes"] = bbox
        return image, target


class RandomHorizontalFlip(object):
    def __init__(self, prob):
        self.prob = prob

    def __call__(self, image, target):
        if random.random() < self.prob:
            height, width = image.shape[-2:]
            image = image.flip(-1)
            bbox = target["boxes"]
            bbox[:, [0, 2]] = width - bbox[:, [2, 0]]
            target["boxes"] = bbox
        return image, target


class GaussianNoise(object):
    def __init__(self, weights=[0.5, 0.3, 0.15, 0.05], prob=[0, 0.05, 0.15, 0.3]):
        self.prob = prob
        self.weights = weights

    def __call__(self, image, target):
        height, width = image.shape[-2:]
        level = random.choices(self.prob, weights=self.weights)[0]
        if level == 0:
            return image, target

        noise_filter = np.zeros(height * width)
        noise_filter[: int(level * height * width)] = 1
        np.random.shuffle(noise_filter)
        noise_filter = noise_filter.reshape((height, width))
        noise = np.random.normal(0, 1, image.shape)
        noise = torch.Tensor(noise * noise_filter)
        image = image + noise
        image[image > 1] = 1
        image[image < 0] = 0
        return image, target


class RandomRotate(object):
    """Randomly rotates an image    
    
    
    Bounding boxes which have an area of less than 25% in the remaining in the 
    transformed image is dropped. The resolution is maintained, and the remaining
    area if any is filled by black color.
    
    Parameters
    ----------
    angle: float or tuple(float)
        if **float**, the image is rotated by a factor drawn 
        randomly from a range (-`angle`, `angle`). If **tuple**,
        the `angle` is drawn randomly from values specified by the 
        tuple
        
    Returns
    -------
    
    numpy.ndaaray
        Rotated image in the numpy format of shape `HxWxC`
    
    numpy.ndarray
        Tranformed bounding box co-ordinates of the format `n x 4` where n is 
        number of bounding boxes and 4 represents `x1,y1,x2,y2` of the box
        
    """

    def __init__(self, angle=30):
        self.angle = angle

        if type(self.angle) == tuple:
            assert len(self.angle) == 2, "Invalid range"

        else:
            self.angle = (-self.angle, self.angle)

    def __call__(self, img, bboxes):
        img = np.array(img)
        angle = random.uniform(*self.angle)
        w, h = 752, 752
        cx, cy = w // 2, h // 2
        img = rotate_im(img, angle)
        corners = get_corners(bboxes["boxes"])
        corners = np.hstack((corners, bboxes["boxes"][:, 4:]))
        corners[:, :8] = rotate_box(corners[:, :8], angle, cx, cy, h, w)
        new_bbox = get_enclosing_box(corners)
        scale_factor_x = img.shape[1] / w
        scale_factor_y = img.shape[0] / h
        img = cv2.resize(img, (w, h))
        new_bbox[:, :4] /= [
            scale_factor_x,
            scale_factor_y,
            scale_factor_x,
            scale_factor_y,
        ]
        bboxes["boxes"] = new_bbox
        bboxes["boxes"] = clip_box(bboxes["boxes"], [0, 0, w, h], 0.25)
        bboxes["boxes"] = torch.from_numpy(bboxes["boxes"])
        return Image.fromarray(img), bboxes


class ToTensor(object):
    def __call__(self, image, target):
        image = F.to_tensor(image)
        return image, target
