#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import os
from bob.gradiant.pad.evaluator import Configuration, EndToEndConfiguration


class TestUtils(object):
    resources_path = os.path.join(os.getcwd(), 'resources')
    result_path = os.path.join(os.getcwd(), 'result')
    configuration_file = os.path.join(resources_path, 'config/config_test.py')
    pipeline_path = os.path.join(resources_path, 'pipeline')

    @classmethod
    def get_resources_path(cls):
        return cls.resources_path

    @classmethod
    def get_result_path(cls):
        return cls.result_path

    @classmethod
    def get_configuration(cls, type_evaluation):
        return Configuration.fromfilename(type_evaluation, cls.configuration_file)

    @classmethod
    def get_end_to_end_configuration(cls):
        return EndToEndConfiguration.fromfilename(cls.configuration_file)

    @classmethod
    def get_pipeline_path(cls):
        return cls.pipeline_path
