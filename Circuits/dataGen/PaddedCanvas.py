import schemdraw
import schemdraw.elements as elm
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import json


class PaddedCanvas(schemdraw.Drawing):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color_code = {
            type(elm.Battery()): "blue",
            type(elm.Capacitor()): "cyan",
            type(elm.Resistor()): "red",
            type(elm.Inductor()): "green",
            type(elm.Diode()): "yellow",
        }

        self.elementNames = {
            type(elm.Battery()): "battery",
            type(elm.Capacitor()): "capacitor",
            type(elm.Resistor()): "resistor",
            type(elm.Inductor()): "inductor",
            type(elm.Diode()): "diode",
        }

        self.elementPos = {
            type(elm.Battery()): 0.37,
            type(elm.Capacitor()): 0.45,
            type(elm.Resistor()): 0.33,
            type(elm.Inductor()): 0.33,
            type(elm.Diode()): 0.4,
        }
        self.inv_color_code = {v: k for k, v in self.color_code.items()}
        self.boundingBoxes = []

    def save(
        self, fname, dpi=72, transparent=False, boxes=False,
    ):
        fig = schemdraw.backends.mpl.Figure(
            ax=None, bbox=None, inches_per_unit=self.inches_per_unit, showframe=False
        )
        for element in self.elements:
            element.draw(fig)
        fig.getfig().savefig(
            f"Data/Images/{fname}", pad_inches=0, transparent=transparent,
        )
        Image.open(f"Data/Images/{fname}").convert("L").save(f"Data/Images/{fname}")
        bboxes = self.getBoundingBoxes()

        data = {
            "name": fname,
            "boxes": [[box[0], self.elementNames[box[1]]] for box in bboxes],
        }

        with open(f"Data/Annotations/{fname[:-4]}.json", "w") as fp:
            json.dump(data, fp, indent=4)

        if boxes:
            self.drawBoundingBoxes(fname, bboxes)
        plt.close("all")

    def transformBoundingBox(self, BBox, padding=5, fdiag=0.95):
        x1, y1 = BBox[0][0]
        x2, y2 = BBox[0][1]
        x_min, x_max, y_min, y_max = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)
        x_min = 104 + 136 * (x_min / 3)
        x_max = 104 + 136 * (x_max / 3)
        y_min = 102 + 128 * (y_min / 3)
        y_max = 102 + 128 * (y_max / 3)

        # Widht Adjustment
        wdelta = self.elementPos[BBox[2]]
        if x_min == x_max:
            y_min += wdelta * 128
            y_max -= wdelta * 128
        elif y_min == y_max:
            x_min += wdelta * 136
            x_max -= wdelta * 136
        else:
            y_min += wdelta * 128 * fdiag
            y_max -= wdelta * 128 * fdiag
            x_min += wdelta * 136 * fdiag
            x_max -= wdelta * 136 * fdiag

        # Height Adjustment
        hdelta_p = abs(BBox[1][0])
        hdelta_n = abs(BBox[1][1])
        if x_min == x_max:
            x_min -= hdelta_n * 46
            x_max += hdelta_p * 46
        elif y_min == y_max:
            y_min -= hdelta_n * 43
            y_max += hdelta_p * 43
        else:
            pass
        return (
            [
                x_min - padding,
                752 - y_max - padding,
                x_max + padding,
                752 - y_min + padding,
            ],
            BBox[2],
        )

    def getBoundingBoxes(self):
        return [self.transformBoundingBox(bbox) for bbox in self.boundingBoxes]

    def drawBoundingBoxes(self, source, boxes):
        im = Image.open(f"Data/Images/{source}").convert("RGB")
        draw = ImageDraw.Draw(im)
        for box in boxes:
            draw.rectangle(
                ((box[0][0], box[0][1]), (box[0][2], box[0][3])),
                outline=self.color_code[box[1]],
                width=1,
            )
        im.save(f"Data/ImagesBB/{source}", "PNG")
