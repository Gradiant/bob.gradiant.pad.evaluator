#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import unittest
import os
import shutil

from bob.gradiant.pad.evaluator.test.test_utils import TestUtils
from bob.gradiant.pad.evaluator import EndToEndEvaluationProtocol


class UnitTestEndToEndEvaluationProtocol(unittest.TestCase):

    def setUp(self):
        self.configuration = TestUtils.get_end_to_end_configuration()
        self.configuration.verbose = False

    def tearDown(self):
        pass
        #if os.path.isdir('result'):
        #    shutil.rmtree('result')

    def test_init_none_configuration(self):
        self.assertRaises(TypeError,
                          lambda: EndToEndEvaluationProtocol(None)
                          )

    def test_init_correct_configuration(self):
        EndToEndEvaluationProtocol(self.configuration)


    def test_run_correct_configuration(self):
        algorithmic_constrained_evaluation_protocol = EndToEndEvaluationProtocol(self.configuration)
        algorithmic_constrained_evaluation_protocol.run()

    '''
    TODO
    def test_run_correct_configuration(self):
          algorithmic_constrained_evaluation_protocol = EndtoEndEvaluationProtocol(self.configuration)
          algorithmic_constrained_evaluation_protocol.run()

          for database in self.configuration.databases:
              root_path = os.path.join(TestUtils.get_result_path(),'ACE', database.name())
              for framerate in self.configuration.framerate_list:
                  for time_capture in self.configuration.total_time_acquisition_list:
                        self.assertTrue(os.path.isdir('{}/features/framerate{}_time_capture{}'.format(root_path,framerate, time_capture)))
              self.assertTrue(os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/configurations'.format(root_path)))
              self.assertTrue(os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/evaluation'.format(root_path)))
              self.assertTrue(os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/experiment_result'.format(root_path)))

    def test_run_configuration_loading_pipeline_from_file_and_skip_training(self):
        configuration = TestUtils.get_configuration('ACE')

        #Modify pipeline
        configuration.pipeline = Pipeline('test_approach_pca095_linear_svc',
                            [Pca(name='Pca', n_components=0.95), LinearSvc(name='LinearSvc')])
        configuration.pipeline.load(TestUtils.get_pipeline_path())

        #Skip training
        configuration.skip_training = True
        configuration.verbose = False

        algorithmic_unconstrained_evaluation_protocol = EndtoEndEvaluationProtocol(configuration)
        algorithmic_unconstrained_evaluation_protocol.run()

        for database in configuration.databases:
            for framerate in self.configuration.framerate_list:
                for time_capture in self.configuration.total_time_acquisition_list:
                    self.assertTrue(os.path.isdir(
                        '{}/ACE/{}/features/framerate{}_time_capture{}'.format(TestUtils.get_result_path(),
                                                                               database.name(),
                                                                               framerate,
                                                                               time_capture)))

        for database in configuration.databases:
            root_path = os.path.join(TestUtils.get_result_path(),'ACE', database.name())
            self.assertTrue(os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/configurations'.format(root_path)))
            self.assertTrue(os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/evaluation'.format(root_path)))
            self.assertTrue(os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/experiment_result'.format(root_path)))


    def test_run_configuration_with_protocol_not_available_on_database_object(self):
        configuration = TestUtils.get_configuration('ACE')

        #Modify protocols list
        configuration.protocols_list = ['no_available_protocol']
        configuration.verbose = False

        algorithmic_constrained_evaluation_protocol = EndtoEndEvaluationProtocol(configuration)

        self.assertRaises(Warning,
                            lambda: algorithmic_constrained_evaluation_protocol.run()
                          )
        for database in configuration.databases:
            for framerate in self.configuration.framerate_list:
                for time_capture in self.configuration.total_time_acquisition_list:
                    self.assertTrue(os.path.isdir(
                        '{}/ACE/{}/features/framerate{}_time_capture{}'.format(TestUtils.get_result_path(),
                                                                               database.name(),
                                                                               framerate,
                                                                               time_capture)))

    def test_run_configuration_loading_features_from_none_dict_extracted_features_paths_and_skip_features_extraction(
            self):
        configuration = TestUtils.get_configuration('ACE')

        # Modify protocols list
        configuration.skip_features_extraction = True
        configuration.dict_extracted_features_paths = None
        configuration.verbose = False

        algorithmic_constrained_evaluation_protocol = AlgorithmicConstrainedEvaluationProtocol(configuration)

        self.assertRaises(Warning,
                          lambda: algorithmic_constrained_evaluation_protocol.run()
                          )

    def test_run_configuration_loading_features_from_correct_path_and_skip_features_extraction(self):
        configuration = TestUtils.get_configuration('ACE')

        # Modify protocols list
        configuration.skip_features_extraction = True
        configuration.dict_extracted_features_paths = {configuration.databases_list[0].name() : os.path.join(TestUtils.get_resources_path(),'features')}
        configuration.verbose = False

        algorithmic_unconstrained_evaluation_protocol = AlgorithmicConstrainedEvaluationProtocol(configuration)
        algorithmic_unconstrained_evaluation_protocol.run()

        for database in configuration.databases:
            root_path = os.path.join(TestUtils.get_result_path(), 'ACE', database.name())
            for framerate in self.configuration.framerate_list:
                for time_capture in self.configuration.total_time_acquisition_list:
                    self.assertTrue(os.path.isdir(
                        '{}/ACE/{}/features/framerate{}_time_capture{}'.format(TestUtils.get_result_path(),
                                                                               database.name(),
                                                                               framerate,
                                                                               time_capture)))
            self.assertTrue(os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/configurations'.format(root_path)))
            self.assertTrue(os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/evaluation'.format(root_path)))
            self.assertTrue(os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/experiment_result'.format(root_path)))


'''