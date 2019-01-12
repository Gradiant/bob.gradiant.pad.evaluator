import numpy as np
from bob.gradiant.pad.evaluator.classes.pad.face_pad import FacePad


class DummyFacePad(FacePad):
    def __init__(self, name = 'DummyFacePad'):
        self.im_array = []
        self.count = 0
        super(DummyFacePad, self).__init__(name)

    def process(self, im):
        self.im_array.append(im)

    def is_finished(self):
        pass

    def reset(self):
        pass

    def get_decision(self):
        self.im_array = []
        self.count += 1
        if self.count % 2:
            return 'ATTACK', np.random.uniform(0, 0.4)
        else:
            return 'NO ATTACK', np.random.uniform(0.6, 1)
