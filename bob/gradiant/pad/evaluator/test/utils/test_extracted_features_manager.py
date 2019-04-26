#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import os
import shutil
import unittest
from bob.gradiant.pad.evaluator import ExtractedFeaturesManager
from bob.gradiant.pad.evaluator.test.test_utils import TestUtils
from bob.gradiant.face.databases import DummyDatabase


class UnitTestExtractedFeaturesManger(unittest.TestCase):
    database_name = 'dummy-database'

    def tearDown(self):
        if os.path.isdir('result'):
            shutil.rmtree('result')

    def test_constructor_none_dict_extracted_features_paths(self):
        dict_extracted_features_paths = None
        self.assertRaises(TypeError,
                          lambda: ExtractedFeaturesManager(dict_extracted_features_paths)
                          )

    def test_constructor_empty_dict_extracted_features_paths(self):
        dict_extracted_features_paths = ""
        self.assertRaises(TypeError,
                          lambda: ExtractedFeaturesManager(dict_extracted_features_paths)
                          )

    def test_constructor_none_value_of_dict_extracted_features_paths(self):
        dict_extracted_features_paths = {'database': {'ACE': None}}
        self.assertRaises(TypeError,
                          lambda: ExtractedFeaturesManager(dict_extracted_features_paths)
                          )

    def test_constructor_empty_value_of_dict_extracted_features_paths(self):
        dict_extracted_features_paths = {'database': ""}
        self.assertRaises(ValueError,
                          lambda: ExtractedFeaturesManager(dict_extracted_features_paths)
                          )

    def test_constructor_fake_dir_value_of_dict_extracted_features_paths(self):
        dict_extracted_features_paths = {'database': "~/features/fake"}
        self.assertRaises(ValueError,
                          lambda: ExtractedFeaturesManager(dict_extracted_features_paths)
                          )

    def test_create_link_for_whole_video_if_database_is_not_a_collection_of_databases(self):
        type_evaluation = 'ACE'
        dict_extracted_features_paths = {self.database_name: {
            type_evaluation: os.path.join(TestUtils.get_resources_path(), 'features')}
        }
        result_path = os.path.join(TestUtils.get_result_path(), 'link_features/whole_video')

        extracted_features_manager = ExtractedFeaturesManager(dict_extracted_features_paths)

        extracted_features_manager.create_features_path_link_to(result_path, DummyDatabase('resources'),
                                                                type_evaluation)

        self.assertTrue(os.path.islink(os.path.join(result_path)))

    def test_create_link_for_15_1000_if_database_is_not_a_collection_of_databases(self):
        type_evaluation = 'ACE'
        dict_extracted_features_paths = {
            self.database_name: {type_evaluation: os.path.join(TestUtils.get_resources_path(), 'features')}}
        result_path = os.path.join(TestUtils.get_result_path(), 'link_features/framerate15_duration1000_startingtime100')

        extracted_features_manager = ExtractedFeaturesManager(dict_extracted_features_paths)

        extracted_features_manager.create_features_path_link_to(result_path,
                                                                DummyDatabase('resources'),
                                                                type_evaluation)

        self.assertTrue(os.path.islink(os.path.join(result_path)))
