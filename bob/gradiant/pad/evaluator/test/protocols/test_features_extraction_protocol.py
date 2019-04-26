#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import unittest
import os
import shutil

from bob.gradiant.pad.evaluator.test.test_utils import TestUtils
from bob.gradiant.pad.evaluator import FeaturesExtractionProtocol


class UnitTestFeaturesExtractionProtocol(unittest.TestCase):

    def setUp(self):
        self.configuration = TestUtils.get_configuration('FE')

    def tearDown(self):
        if os.path.isdir('result'):
            shutil.rmtree('result')

    def test_init_none_configuration(self):
        self.assertRaises(TypeError, lambda: FeaturesExtractionProtocol(None))

    def test_init_correct_configuration(self):
        FeaturesExtractionProtocol(TestUtils.get_configuration('FE'))

    def test_run_default_configuration(self):
        self.configuration.verbose = False
        features_extraction_protocol = FeaturesExtractionProtocol(self.configuration)
        features_extraction_protocol.run()

        for database in self.configuration.databases_list:
            root_path = os.path.join(TestUtils.get_result_path(), 'FE', database.name())

            for parameters in self.configuration.access_grid_config.get_parameter_grid():
                self.assertTrue(os.path.isdir(
                    '{}/features/framerate{}_duration{}_startingtime{}'.format(root_path,
                                                                               parameters['framerate'],
                                                                               parameters[
                                                                                   'total_time_acquisition'],
                                                                               parameters[
                                                                                   'starting_time_acquisition'])))
