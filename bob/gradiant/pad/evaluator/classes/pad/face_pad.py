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
    def is_finished(self):
        raise NotImplementedError

    @abstractmethod
    def reset(self):
        raise NotImplementedError

    @abstractmethod
    def get_decision(self):
        raise NotImplementedError
