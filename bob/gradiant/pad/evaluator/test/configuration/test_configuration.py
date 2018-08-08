#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import unittest
import os
import shutil
from bob.gradiant.pad.evaluator import Configuration
from bob.gradiant.core import DummyFeaturesExtractor
from bob.gradiant.pad.evaluator import DummyDatabase
from bob.gradiant.pipelines import Pipeline, Pca, LinearSvc


class UnitTestConfiguration(unittest.TestCase):

    configuration_file = 'resources/config/config_test.py'
    databases = [DummyDatabase('resources')]
    protocols = ['grandtest']
    feature_extractor = DummyFeaturesExtractor()
    pipeline = Pipeline('pca095_linear_svc', [Pca(name='Pca', n_components=0.95), LinearSvc(name='LinearSvc')])
    result_path = 'result'
    framerate_list = [5, 10, 15, 20, 25]
    total_time_acquisition_list = [500, 1000, 1500, 2000]
    verbose = True
    number_threads = 1
    use_data_augmentation = False
    skip_features_extraction = False
    dict_extracted_features_paths = None
    skip_training = False
    skip_scores_prediction = False
    dict_scores_prediction = None
    recreate = False

    def tearDown(self):
        if os.path.isdir('result'):
            shutil.rmtree('result')

    def test_init_fromfilename_wrong_path(self):
        self.assertRaises(IOError,
                          lambda: Configuration.fromfilename('ACE','WRONG')
                          )

    def test_init_fromfilename_wrong_type_evaluation(self):
        self.assertRaises(ValueError,
                          lambda: Configuration.fromfilename('WRONG', self.configuration_file)
                          )

    def test_init_fromfilename_correct_params(self):
        Configuration.fromfilename('ACE', self.configuration_file)

    def test_init_correct_params_but_database_path_not_defined(self):

        replay_path = None
        if "REPLAY_ATTACK_PATH" in os.environ:
            replay_path =  os.environ["REPLAY_ATTACK_PATH"]
            del os.environ["REPLAY_ATTACK_PATH"]

        self.assertRaises(EnvironmentError,
                          lambda: Configuration('ACE',
                                                ['replay-attack'],
                                                self.protocols,
                                                self.feature_extractor,
                                                self.pipeline,
                                                self.result_path,
                                                framerate_list = self.framerate_list,
                                                total_time_acquisition_list = self.total_time_acquisition_list,
                                                verbose = self.verbose,
                                                number_threads = self.number_threads,
                                                use_data_augmentation = self.use_data_augmentation,
                                                skip_features_extraction = self.skip_features_extraction,
                                                dict_extracted_features_paths= self.dict_extracted_features_paths,
                                                skip_training = self.skip_training,
                                                skip_scores_prediction=self.skip_scores_prediction,
                                                dict_scores_prediction = self.dict_scores_prediction,
                                                recreate = self.recreate)
                          )

        if replay_path:
            os.environ["REPLAY_ATTACK_PATH"] = replay_path

    def test_init_incorrect_databases_param(self):
        self.assertRaises(TypeError,
                          lambda: Configuration('ACE',
                                                'WRONG_PARAM',
                                                self.protocols,
                                                self.feature_extractor,
                                                self.pipeline,
                                                self.result_path,
                                                framerate_list=self.framerate_list,
                                                total_time_acquisition_list=self.total_time_acquisition_list,
                                                verbose=self.verbose,
                                                number_threads=self.number_threads,
                                                use_data_augmentation=self.use_data_augmentation,
                                                skip_features_extraction=self.skip_features_extraction,
                                                dict_extracted_features_paths=self.dict_extracted_features_paths,
                                                skip_training=self.skip_training,
                                                skip_scores_prediction=self.skip_scores_prediction,
                                                dict_scores_prediction=self.dict_scores_prediction,
                                                recreate=self.recreate)
                          )

    def test_init_incorrect_databases_param_no_exist(self):
        self.assertRaises(ValueError,
                          lambda: Configuration('ACE',
                                                ['no_exist_database'],
                                                self.protocols,
                                                self.feature_extractor,
                                                self.pipeline,
                                                self.result_path,
                                                framerate_list=self.framerate_list,
                                                total_time_acquisition_list=self.total_time_acquisition_list,
                                                verbose=self.verbose,
                                                number_threads=self.number_threads,
                                                use_data_augmentation=self.use_data_augmentation,
                                                skip_features_extraction=self.skip_features_extraction,
                                                dict_extracted_features_paths=self.dict_extracted_features_paths,
                                                skip_training=self.skip_training,
                                                skip_scores_prediction=self.skip_scores_prediction,
                                                dict_scores_prediction=self.dict_scores_prediction,
                                                recreate=self.recreate)
                          )

    def test_init_incorrect_protocol_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: Configuration('ACE',
                                                self.databases,
                                                'WRONG_PARAM',
                                                self.feature_extractor,
                                                self.pipeline,
                                                self.result_path,
                                                framerate_list=self.framerate_list,
                                                total_time_acquisition_list=self.total_time_acquisition_list,
                                                verbose=self.verbose,
                                                number_threads=self.number_threads,
                                                use_data_augmentation=self.use_data_augmentation,
                                                skip_features_extraction=self.skip_features_extraction,
                                                dict_extracted_features_paths=self.dict_extracted_features_paths,
                                                skip_training=self.skip_training,
                                                skip_scores_prediction=self.skip_scores_prediction,
                                                dict_scores_prediction=self.dict_scores_prediction,
                                                recreate=self.recreate)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_incorrect_features_extractor_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: Configuration('ACE',
                                                self.databases,
                                                self.protocols,
                                                "WRONG_PARAM",
                                                self.pipeline,
                                                self.result_path,
                                                framerate_list=self.framerate_list,
                                                total_time_acquisition_list=self.total_time_acquisition_list,
                                                verbose=self.verbose,
                                                number_threads=self.number_threads,
                                                use_data_augmentation=self.use_data_augmentation,
                                                skip_features_extraction=self.skip_features_extraction,
                                                dict_extracted_features_paths=self.dict_extracted_features_paths,
                                                skip_training=self.skip_training,
                                                skip_scores_prediction=self.skip_scores_prediction,
                                                dict_scores_prediction=self.dict_scores_prediction,
                                                recreate=self.recreate)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_incorrect_pipeline_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: Configuration('ACE',
                                                self.databases,
                                                self.protocols,
                                                self.feature_extractor,
                                                "WRONG_PARAM",
                                                self.result_path,
                                                framerate_list=self.framerate_list,
                                                total_time_acquisition_list=self.total_time_acquisition_list,
                                                verbose=self.verbose,
                                                number_threads=self.number_threads,
                                                use_data_augmentation=self.use_data_augmentation,
                                                skip_features_extraction=self.skip_features_extraction,
                                                dict_extracted_features_paths=self.dict_extracted_features_paths,
                                                skip_training=self.skip_training,
                                                skip_scores_prediction=self.skip_scores_prediction,
                                                dict_scores_prediction=self.dict_scores_prediction,
                                                recreate=self.recreate)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]


    def test_init_none_result_path_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: Configuration('ACE',
                                                self.databases,
                                                self.protocols,
                                                self.feature_extractor,
                                                self.pipeline,
                                                None,
                                                framerate_list=self.framerate_list,
                                                total_time_acquisition_list=self.total_time_acquisition_list,
                                                verbose=self.verbose,
                                                number_threads=self.number_threads,
                                                use_data_augmentation=self.use_data_augmentation,
                                                skip_features_extraction=self.skip_features_extraction,
                                                dict_extracted_features_paths=self.dict_extracted_features_paths,
                                                skip_training=self.skip_training,
                                                skip_scores_prediction=self.skip_scores_prediction,
                                                dict_scores_prediction=self.dict_scores_prediction,
                                                recreate=self.recreate)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_incorrect_result_path_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: Configuration('ACE',
                                                self.databases,
                                                self.protocols,
                                                self.feature_extractor,
                                                self.pipeline,
                                                ['WRONG_PARAM'],
                                                framerate_list=self.framerate_list,
                                                total_time_acquisition_list=self.total_time_acquisition_list,
                                                verbose=self.verbose,
                                                number_threads=self.number_threads,
                                                use_data_augmentation=self.use_data_augmentation,
                                                skip_features_extraction=self.skip_features_extraction,
                                                dict_extracted_features_paths=self.dict_extracted_features_paths,
                                                skip_training=self.skip_training,
                                                skip_scores_prediction=self.skip_scores_prediction,
                                                dict_scores_prediction=self.dict_scores_prediction,
                                                recreate=self.recreate)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_none_framerate_list_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: Configuration('ACE',
                                                self.databases,
                                                self.protocols,
                                                self.feature_extractor,
                                                self.pipeline,
                                                self.result_path,
                                                framerate_list=None,
                                                total_time_acquisition_list=self.total_time_acquisition_list,
                                                verbose=self.verbose,
                                                number_threads=self.number_threads,
                                                use_data_augmentation=self.use_data_augmentation,
                                                skip_features_extraction=self.skip_features_extraction,
                                                dict_extracted_features_paths=self.dict_extracted_features_paths,
                                                skip_training=self.skip_training,
                                                skip_scores_prediction=self.skip_scores_prediction,
                                                dict_scores_prediction=self.dict_scores_prediction,
                                                recreate=self.recreate)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_incorrect_framerate_list_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: Configuration('ACE',
                                                self.databases,
                                                self.protocols,
                                                self.feature_extractor,
                                                self.pipeline,
                                                self.result_path,
                                                framerate_list="WRONG_PARAMETER",
                                                total_time_acquisition_list=self.total_time_acquisition_list,
                                                verbose=self.verbose,
                                                number_threads=self.number_threads,
                                                use_data_augmentation=self.use_data_augmentation,
                                                skip_features_extraction=self.skip_features_extraction,
                                                dict_extracted_features_paths=self.dict_extracted_features_paths,
                                                skip_training=self.skip_training,
                                                skip_scores_prediction=self.skip_scores_prediction,
                                                dict_scores_prediction=self.dict_scores_prediction,
                                                recreate=self.recreate)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]


    def test_init_none_total_time_acquisition_list_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: Configuration('ACE',
                                                self.databases,
                                                self.protocols,
                                                self.feature_extractor,
                                                self.pipeline,
                                                self.result_path,
                                                framerate_list=self.framerate_list,
                                                total_time_acquisition_list=None,
                                                verbose=self.verbose,
                                                number_threads=self.number_threads,
                                                use_data_augmentation=self.use_data_augmentation,
                                                skip_features_extraction=self.skip_features_extraction,
                                                dict_extracted_features_paths=self.dict_extracted_features_paths,
                                                skip_training=self.skip_training,
                                                skip_scores_prediction=self.skip_scores_prediction,
                                                dict_scores_prediction=self.dict_scores_prediction,
                                                recreate=self.recreate)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_incorrect_total_time_acquisition_list_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: Configuration('ACE',
                                                self.databases,
                                                self.protocols,
                                                self.feature_extractor,
                                                self.pipeline,
                                                self.result_path,
                                                framerate_list=self.framerate_list,
                                                total_time_acquisition_list="WRONG_PARAMETER",
                                                verbose=self.verbose,
                                                number_threads=self.number_threads,
                                                use_data_augmentation=self.use_data_augmentation,
                                                skip_features_extraction=self.skip_features_extraction,
                                                dict_extracted_features_paths=self.dict_extracted_features_paths,
                                                skip_training=self.skip_training,
                                                skip_scores_prediction=self.skip_scores_prediction,
                                                dict_scores_prediction=self.dict_scores_prediction,
                                                recreate=self.recreate)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_none_verbose_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: Configuration('ACE',
                                                self.databases,
                                                self.protocols,
                                                self.feature_extractor,
                                                self.pipeline,
                                                self.result_path,
                                                framerate_list=self.framerate_list,
                                                total_time_acquisition_list=self.total_time_acquisition_list,
                                                verbose=None,
                                                number_threads=self.number_threads,
                                                use_data_augmentation=self.use_data_augmentation,
                                                skip_features_extraction=self.skip_features_extraction,
                                                dict_extracted_features_paths=self.dict_extracted_features_paths,
                                                skip_training=self.skip_training,
                                                skip_scores_prediction=self.skip_scores_prediction,
                                                dict_scores_prediction=self.dict_scores_prediction,
                                                recreate=self.recreate)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_wrong_verbose_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: Configuration('ACE',
                                                self.databases,
                                                self.protocols,
                                                self.feature_extractor,
                                                self.pipeline,
                                                self.result_path,
                                                framerate_list=self.framerate_list,
                                                total_time_acquisition_list=self.total_time_acquisition_list,
                                                verbose='WRONG',
                                                number_threads=self.number_threads,
                                                use_data_augmentation=self.use_data_augmentation,
                                                skip_features_extraction=self.skip_features_extraction,
                                                dict_extracted_features_paths=self.dict_extracted_features_paths,
                                                skip_training=self.skip_training,
                                                skip_scores_prediction=self.skip_scores_prediction,
                                                dict_scores_prediction=self.dict_scores_prediction,
                                                recreate=self.recreate)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_none_number_threads_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: Configuration('ACE',
                                                self.databases,
                                                self.protocols,
                                                self.feature_extractor,
                                                self.pipeline,
                                                self.result_path,
                                                framerate_list=self.framerate_list,
                                                total_time_acquisition_list=self.total_time_acquisition_list,
                                                verbose=self.verbose,
                                                number_threads=None,
                                                use_data_augmentation=self.use_data_augmentation,
                                                skip_features_extraction=self.skip_features_extraction,
                                                dict_extracted_features_paths=self.dict_extracted_features_paths,
                                                skip_training=self.skip_training,
                                                skip_scores_prediction=self.skip_scores_prediction,
                                                dict_scores_prediction=self.dict_scores_prediction,
                                                recreate=self.recreate)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_none_use_data_augmentation_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: Configuration('ACE',
                                                self.databases,
                                                self.protocols,
                                                self.feature_extractor,
                                                self.pipeline,
                                                self.result_path,
                                                framerate_list=self.framerate_list,
                                                total_time_acquisition_list=self.total_time_acquisition_list,
                                                verbose=self.verbose,
                                                number_threads=self.number_threads,
                                                use_data_augmentation=None,
                                                skip_features_extraction=self.skip_features_extraction,
                                                dict_extracted_features_paths=self.dict_extracted_features_paths,
                                                skip_training=self.skip_training,
                                                skip_scores_prediction=self.skip_scores_prediction,
                                                dict_scores_prediction=self.dict_scores_prediction,
                                                recreate=self.recreate)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_none_skip_features_extraction_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: Configuration('ACE',
                                                self.databases,
                                                self.protocols,
                                                self.feature_extractor,
                                                self.pipeline,
                                                self.result_path,
                                                framerate_list=self.framerate_list,
                                                total_time_acquisition_list=self.total_time_acquisition_list,
                                                verbose=self.verbose,
                                                number_threads=self.number_threads,
                                                use_data_augmentation=self.use_data_augmentation,
                                                skip_features_extraction=None,
                                                dict_extracted_features_paths=self.dict_extracted_features_paths,
                                                skip_training=self.skip_training,
                                                skip_scores_prediction=self.skip_scores_prediction,
                                                dict_scores_prediction=self.dict_scores_prediction,
                                                recreate=self.recreate)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_none_skip_training_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: Configuration('ACE',
                                                self.databases,
                                                self.protocols,
                                                self.feature_extractor,
                                                self.pipeline,
                                                self.result_path,
                                                framerate_list=self.framerate_list,
                                                total_time_acquisition_list=self.total_time_acquisition_list,
                                                verbose=self.verbose,
                                                number_threads=self.number_threads,
                                                use_data_augmentation=self.use_data_augmentation,
                                                skip_features_extraction=self.skip_features_extraction,
                                                dict_extracted_features_paths=self.dict_extracted_features_paths,
                                                skip_training=None,
                                                skip_scores_prediction=self.skip_scores_prediction,
                                                dict_scores_prediction=self.dict_scores_prediction,
                                                recreate=self.recreate)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_none_skip_scores_prediction(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: Configuration('ACE',
                                                self.databases,
                                                self.protocols,
                                                self.feature_extractor,
                                                self.pipeline,
                                                self.result_path,
                                                framerate_list=self.framerate_list,
                                                total_time_acquisition_list=self.total_time_acquisition_list,
                                                verbose=self.verbose,
                                                number_threads=self.number_threads,
                                                use_data_augmentation=self.use_data_augmentation,
                                                skip_features_extraction=self.skip_features_extraction,
                                                dict_extracted_features_paths=self.dict_extracted_features_paths,
                                                skip_training=self.skip_training,
                                                skip_scores_prediction=None,
                                                dict_scores_prediction=self.dict_scores_prediction,
                                                recreate=self.recreate)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]


    def test_init_none_recreate_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: Configuration('ACE',
                                                self.databases,
                                                self.protocols,
                                                self.feature_extractor,
                                                self.pipeline,
                                                self.result_path,
                                                framerate_list=self.framerate_list,
                                                total_time_acquisition_list=self.total_time_acquisition_list,
                                                verbose=self.verbose,
                                                number_threads=self.number_threads,
                                                use_data_augmentation=self.use_data_augmentation,
                                                skip_features_extraction=self.skip_features_extraction,
                                                dict_extracted_features_paths=self.dict_extracted_features_paths,
                                                skip_training=self.skip_training,
                                                skip_scores_prediction=self.skip_scores_prediction,
                                                dict_scores_prediction=self.dict_scores_prediction,
                                                recreate=None)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_print_to_file(self):
        filename_result = 'result/configuration.txt'
        configuration = Configuration.fromfilename('ACE', self.configuration_file)
        configuration.save_to_file(filename_result)
        self.assertTrue(os.path.isfile(filename_result))





