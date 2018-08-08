#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
import os
import shutil

from bob.gradiant.pad.evaluator.test.test_utils import TestUtils
from bob.gradiant.pad.evaluator import AlgorithmicConstrainedEvaluationProtocol
from bob.gradiant.pipelines import LinearSvc
from bob.gradiant.pipelines import Pca
from bob.gradiant.pipelines import Pipeline


class UnitTestAlgorithmicConstrainedEvaluationProtocol(unittest.TestCase):

    def setUp(self):
        self.configuration = TestUtils.get_configuration('ACE')
        self.configuration.verbose = False

    def tearDown(self):
        if os.path.isdir('result'):
            shutil.rmtree('result')

    def test_init_none_configuration(self):
        self.assertRaises(TypeError,
                          lambda: AlgorithmicConstrainedEvaluationProtocol(None)
                          )

    def test_init_correct_configuration(self):
        AlgorithmicConstrainedEvaluationProtocol(self.configuration)

    def test_run_correct_configuration(self):
          algorithmic_constrained_evaluation_protocol = AlgorithmicConstrainedEvaluationProtocol(self.configuration)
          algorithmic_constrained_evaluation_protocol.run()

          for database in self.configuration.databases_list:
              root_path = os.path.join(TestUtils.get_result_path(),'ACE', database.name())
              for framerate in self.configuration.framerate_list:
                  for time_capture in self.configuration.total_time_acquisition_list:
                        self.assertTrue(os.path.isdir('{}/features/framerate{}_time_capture{}'.format(root_path,framerate, time_capture)))
              self.assertTrue(os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/configurations'.format(root_path)))
              self.assertTrue(os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/evaluation'.format(root_path)))
              self.assertTrue(os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/experiment_result'.format(root_path)))

    def test_run_configuration_loading_pipeline_from_file_and_skip_training(self):
        #Modifying pipeline
        self.configuration.pipeline = Pipeline('test_approach_pca095_linear_svc',
                            [Pca(name='Pca', n_components=0.95), LinearSvc(name='LinearSvc')])
        self.configuration.pipeline.load(TestUtils.get_pipeline_path())

        #Skipping training
        self.configuration.skip_training = True
        self.configuration.verbose = False

        algorithmic_unconstrained_evaluation_protocol = AlgorithmicConstrainedEvaluationProtocol(self.configuration)
        algorithmic_unconstrained_evaluation_protocol.run()

        for database in self.configuration.databases_list:
            for framerate in self.configuration.framerate_list:
                for time_capture in self.configuration.total_time_acquisition_list:
                    self.assertTrue(os.path.isdir(
                        '{}/ACE/{}/features/framerate{}_time_capture{}'.format(TestUtils.get_result_path(),
                                                                               database.name(),
                                                                               framerate,
                                                                               time_capture)))

        for database in self.configuration.databases_list:
            root_path = os.path.join(TestUtils.get_result_path(),'ACE', database.name())
            self.assertTrue(os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/configurations'.format(root_path)))
            self.assertTrue(os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/evaluation'.format(root_path)))
            self.assertTrue(os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/experiment_result'.format(root_path)))


    def test_run_configuration_with_protocol_not_available_on_database_object(self):
        #Modifying protocols list
        self.configuration.protocols_list = ['no_available_protocol']
        self.configuration.verbose = False

        algorithmic_constrained_evaluation_protocol = AlgorithmicConstrainedEvaluationProtocol(self.configuration)

        self.assertRaises(Warning,
                            lambda: algorithmic_constrained_evaluation_protocol.run()
                          )
        for database in self.configuration.databases_list:
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
        # Modifying protocols list
        self.configuration.skip_features_extraction = True
        self.configuration.dict_extracted_features_paths = {self.configuration.databases_list[0].name() : os.path.join(TestUtils.get_resources_path(),'features')}
        self.configuration.verbose = False

        algorithmic_unconstrained_evaluation_protocol = AlgorithmicConstrainedEvaluationProtocol(self.configuration)
        algorithmic_unconstrained_evaluation_protocol.run()

        for database in self.configuration.databases_list:
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

    def test_run_configuration_loading_scores_from_correct_path_and_skip_scores_prediction(self):
        # Modifying skip_scores_prediction
        self.configuration.skip_scores_prediction = True
        self.configuration.dict_scores_prediction = {self.configuration.databases_list[0].name():
                                                         {'ACE': os.path.join(TestUtils.get_resources_path(),
                                                                              'experiment_result')}}

        algorithmic_constrained_evaluation_protocol = AlgorithmicConstrainedEvaluationProtocol(self.configuration)
        algorithmic_constrained_evaluation_protocol.run()

        for database in self.configuration.databases_list:
            root_path = os.path.join(TestUtils.get_result_path(), 'ACE', database.name())
            self.assertTrue(os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/evaluation'.format(root_path)))

            for protocol in self.configuration.protocols_list:
                for subset in ['Train', 'Dev', 'Test']:
                    for framerate in self.configuration.framerate_list:
                        for total_time_of_acquisition in self.configuration.total_time_acquisition_list:
                            link_path = '{}/pipelines/test_approach_pca095_linear_svc/experiment_result/{}/{}/{}_{}.h5'\
                                .format(root_path,
                                        protocol,
                                        subset,
                                        framerate,
                                        total_time_of_acquisition)
                            self.assertTrue(os.path.islink(link_path))



