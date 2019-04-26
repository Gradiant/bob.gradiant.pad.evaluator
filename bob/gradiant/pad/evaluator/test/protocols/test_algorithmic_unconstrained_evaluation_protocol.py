#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import unittest
import os
import shutil

from bob.gradiant.pad.evaluator.test.test_utils import TestUtils
from bob.gradiant.pad.evaluator import AlgorithmicUnconstrainedEvaluationProtocol
from bob.gradiant.pipelines import LinearSvc
from bob.gradiant.pipelines import Pca
from bob.gradiant.pipelines import Pipeline


class UnitTestAlgorithmicUnconstrainedEvaluationProtocol(unittest.TestCase):

    def setUp(self):
        self.configuration = TestUtils.get_configuration('AUE')

    def tearDown(self):
        if os.path.isdir('result'):
            shutil.rmtree('result')

    def test_init_none_configuration(self):
        self.assertRaises(TypeError, lambda: AlgorithmicUnconstrainedEvaluationProtocol(None))

    def test_init_correct_configuration(self):
        AlgorithmicUnconstrainedEvaluationProtocol(TestUtils.get_configuration('AUE'))

    def test_run_default_configuration(self):
        self.configuration.verbose = False
        algorithmic_unconstrained_evaluation_protocol = AlgorithmicUnconstrainedEvaluationProtocol(self.configuration)
        algorithmic_unconstrained_evaluation_protocol.run()

        for database in self.configuration.databases_list:
            root_path = os.path.join(TestUtils.get_result_path(), 'AUE', database.name())
            self.assertTrue(os.path.isdir('{}/features/whole_video'.format(root_path)))
            self.assertTrue(
                os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/configurations'.format(root_path)))
            self.assertTrue(os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/evaluation'.format(root_path)))
            self.assertTrue(
                os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/experiment_result'.format(root_path)))

    def test_run_configuration_loading_pipeline_from_file_and_skip_training(self):
        self.configuration.verbose = False
        # Modifying pipeline
        self.configuration.pipeline = Pipeline('test_approach_pca095_linear_svc',
                                               [Pca(name='Pca', n_components=0.95), LinearSvc(name='LinearSvc')])
        self.configuration.pipeline.load(TestUtils.get_pipeline_path())

        # Skipping training
        self.configuration.skip_training = True

        algorithmic_unconstrained_evaluation_protocol = AlgorithmicUnconstrainedEvaluationProtocol(self.configuration)
        algorithmic_unconstrained_evaluation_protocol.run()

        for database in self.configuration.databases_list:
            root_path = os.path.join(TestUtils.get_result_path(), 'AUE', database.name())
            self.assertTrue(os.path.isdir('{}/features/whole_video'.format(root_path)))
            self.assertTrue(
                os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/configurations'.format(root_path)))
            self.assertTrue(os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/evaluation'.format(root_path)))
            self.assertTrue(
                os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/experiment_result'.format(root_path)))

    def test_run_configuration_with_protocol_not_available_on_database_object(self):
        # Modifying protocols list
        self.configuration.protocols_list = ['no_available_protocol']

        algorithmic_unconstrained_evaluation_protocol = AlgorithmicUnconstrainedEvaluationProtocol(self.configuration)

        self.assertRaises(Warning,
                          lambda: algorithmic_unconstrained_evaluation_protocol.run()
                          )

        for database in self.configuration.databases_list:
            root_path = os.path.join(TestUtils.get_result_path(), 'AUE', database.name())
            self.assertTrue(os.path.isdir('{}/features/whole_video'.format(root_path)))

    def test_run_configuration_loading_features_from_none_dict_extracted_features_paths_and_skip_features_extraction(
            self):

        # Modify protocols list
        self.configuration.skip_features_extraction = True
        self.configuration.dict_extracted_features_paths = None

        algorithmic_unconstrained_evaluation_protocol = AlgorithmicUnconstrainedEvaluationProtocol(self.configuration)

        self.assertRaises(Warning,
                          lambda: algorithmic_unconstrained_evaluation_protocol.run()
                          )

    def test_run_configuration_loading_features_from_correct_path_and_skip_features_extraction(self):
        # Modifying skip_features_extraction
        self.configuration.skip_features_extraction = True
        self.configuration.dict_extracted_features_paths = {
            self.configuration.databases_list[0].name():
                {'AUE': os.path.join(TestUtils.get_resources_path(), 'features')}}

        algorithmic_unconstrained_evaluation_protocol = AlgorithmicUnconstrainedEvaluationProtocol(self.configuration)
        algorithmic_unconstrained_evaluation_protocol.run()

        for database in self.configuration.databases_list:
            root_path = os.path.join(TestUtils.get_result_path(), 'AUE', database.name())
            self.assertTrue(os.path.isdir('{}/features/whole_video'.format(root_path)))
            self.assertTrue(
                os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/configurations'.format(root_path)))
            self.assertTrue(os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/evaluation'.format(root_path)))
            self.assertTrue(
                os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/experiment_result'.format(root_path)))

    def test_run_configuration_loading_scores_from_correct_path_and_skip_scores_prediction(self):
        # Modifying skip_scores_prediction
        self.configuration.skip_scores_prediction = True

        self.configuration.dict_scores_prediction = {self.configuration.databases_list[0].name():
                                                         {'AUE': os.path.join(TestUtils.get_resources_path(),
                                                                              'experiment_result')}}

        algorithmic_unconstrained_evaluation_protocol = AlgorithmicUnconstrainedEvaluationProtocol(self.configuration)
        algorithmic_unconstrained_evaluation_protocol.run()

        for database in self.configuration.databases_list:
            root_path = os.path.join(TestUtils.get_result_path(), 'AUE', database.name())
            self.assertTrue(os.path.isdir('{}/pipelines/test_approach_pca095_linear_svc/evaluation'.format(root_path)))

            for protocol in self.configuration.protocols_list:
                for subset in ['Train', 'Dev', 'Test']:
                    link_path = '{}/pipelines/test_approach_pca095_linear_svc/experiment_result/{}/{}/whole_video.h5' \
                        .format(root_path,
                                protocol,
                                subset)
                    self.assertTrue(os.path.islink(link_path))
