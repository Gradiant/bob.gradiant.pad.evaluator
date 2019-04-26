from abc import ABCMeta, abstractmethod


class FacePad(object):
    """
    This class declares an abstract interface for face-PAD
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, name, threshold):
        """
          This is a constructor

          :param name: name of the face-PAD. i.e 'TextureBasedFacePad'
          :param threshold:  Decision Threshold to know whether or not the evaluated images belong to a genuine user
        """
        self.name = name
        self.threshold = threshold
        self.finished = False

    @abstractmethod
    def process(self, im):
        raise NotImplementedError

    @abstractmethod
    def isfinished(self):
        raise NotImplementedError

    @abstractmethod
    def reset(self):
        raise NotImplementedError

    @abstractmethod
    def get_decission(self):
        raise NotImplementedError
