#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
from .symlink_force import *

class ExtractedFeaturesManager():

    def __init__(self, dict_extracted_features_paths):

        if not isinstance(dict_extracted_features_paths, dict):
            raise TypeError('dict_extracted_features_paths must be a dict')

        for key, values in dict_extracted_features_paths.iteritems():

            if not isinstance(values, str):
                raise TypeError('dict_extracted_features_paths[\'{}\'] must be a string value'.format(key))

            if not os.path.isdir(values):
                raise ValueError('dict_extracted_features_paths[\'{}\'] must be a correct dir'.format(key))

        self.dict_extracted_features_paths=dict_extracted_features_paths

    def create_features_path_link_to(self, result_path, database):

        basename = os.path.basename(result_path)

        for key, value in self.dict_extracted_features_paths.iteritems():

            if not self.__check_target_folder(self.dict_extracted_features_paths[key], basename):
                raise ValueError("{} target folder is not available on dict_extracted_features_paths[\'{}\'] = "
                                 "\'{}\'".format(basename,key, self.dict_extracted_features_paths))

            if database.is_a_collection_of_databases():
                result_path_features = os.path.join(result_path,key)
            else:
                result_path_features = os.path.join(result_path)

            if not os.path.isdir(os.path.dirname(result_path_features)):
                os.makedirs(os.path.dirname(result_path_features))

            source_path_features = os.path.join(self.dict_extracted_features_paths[key],basename)

            symlink_force(source_path_features, result_path_features)

    def __check_target_folder(self, extracted_features_path, basename):
        exist = False
        for basename_dir in os.listdir(extracted_features_path):
            if os.path.isdir(os.path.join(extracted_features_path, basename_dir)):
                if basename == basename_dir:
                    exist = True
                    break
        return exist


