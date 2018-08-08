from abc import ABCMeta, abstractmethod


class FacePad(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, name):
        self.name = name
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
