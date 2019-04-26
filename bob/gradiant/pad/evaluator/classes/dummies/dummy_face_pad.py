import numpy as np
from bob.gradiant.pad.evaluator.classes.pad.face_pad import FacePad


class DummyFacePad(FacePad):
    def __init__(self, name = 'DummyFacePad', threshold = 0.0):
        self.im_array = []
        self.count = 0
        super(DummyFacePad, self).__init__(name, threshold)

    def process(self, im):
        self.im_array.append(im)

    def isfinished(self):
        pass

    def reset(self):
        pass

    def get_decission(self):
        self.im_array = []
        self.count += 1
        if self.count % 2:
            return 'ATTACK', np.random.uniform(0, 0.4)
        else:
            return 'NO ATTACK', np.random.uniform(0.6, 1)
