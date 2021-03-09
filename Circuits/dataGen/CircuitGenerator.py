from dataGen.GridGenerator import GridGenerator
from dataGen.PaddedCanvas import PaddedCanvas
from random import choice, randint
import schemdraw
import schemdraw.elements as elm


class CircuitGenerator(GridGenerator):
    def __init__(self, x_lim=10, y_lim=10, scale=5, random_state=42):
        super().__init__(x_lim, y_lim, scale, random_state)
        self.elemList = [
            elm.Battery,
            elm.Line,
            elm.Capacitor,
            elm.Inductor,
            elm.Resistor,
            elm.Diode,
        ]

    def generateCircuit(self, lines, l_flag=True):
        canvas = PaddedCanvas()
        for line in lines[:-4]:
            elem = choice(self.elemList)
            if l_flag:
                if elem == elm.Battery:
                    label = str(randint(1, 100)) + "V"
                elif elem == elm.Capacitor:
                    label = str(randint(1, 100)) + "$\mu$F"
                elif elem == elm.Resistor:
                    label = str(round((randint(1, 25) / 10), 2)) + "K$\Omega$"
                elif elem == elm.Inductor:
                    label = str(randint(1, 100)) + "L"
                else:
                    label = None
                canvas.add(elem(endpts=line, label=label))
            else:
                canvas.add(elem(endpts=line))
            if not elem == elm.Line:
                box = elem(endpts=line).get_bbox()
                height = (box.ymin, box.ymax)
                canvas.boundingBoxes.append((line, height, elem))

        for line in lines[-4:]:
            canvas.add(elm.Line(lw=0, endpts=line))
        return canvas
