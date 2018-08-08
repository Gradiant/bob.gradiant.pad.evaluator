#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain

from abc import ABCMeta, abstractmethod

from bob.gradiant.pad.evaluator.classes.configuration.configuration import Configuration
from bob.gradiant.pad.evaluator.classes.configuration.end_to_end_configuration import EndToEndConfiguration


class EvaluationProtocol(object):
    __metaclass__ = ABCMeta

    def __init__(self, configuration):
        if not isinstance(configuration, Configuration) and not isinstance(configuration, EndToEndConfiguration):
            raise TypeError("input must be a Configuration or EndToEndConfiguration")
        self.configuration = configuration

    @abstractmethod
    def run(self):
        raise NotImplementedError
