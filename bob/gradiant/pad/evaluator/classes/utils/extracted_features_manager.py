#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
from .symlink_force import *

try:
    basestring
except NameError:
    basestring = str


class ExtractedFeaturesManager:

    def __init__(self, dict_extracted_features_paths):

        if not isinstance(dict_extracted_features_paths, dict):
            raise TypeError('dict_extracted_features_paths must be a dict')

        for key, dict_extracted_features_path_protocol in dict_extracted_features_paths.items():

            if not isinstance(key, basestring):
                raise TypeError(
                    'dict_extracted_features_paths[\'{}\'] must be a string value (i.e \'database\')'.format(key))

            if not isinstance(dict_extracted_features_path_protocol, dict):
                example = '(i.e {\'ACE\' : \'<path-to-features\'})'
                raise ValueError(
                    'dict_extracted_features_paths value must be a dict with protocol + path ({})'.format(key, example))

            for key, values in dict_extracted_features_path_protocol.items():
                if not isinstance(values, basestring):
                    raise TypeError(
                        'dict_extracted_features_paths[\'name_database\'][\'{}\'] must be a string value (i.e \'ACE\' or \'AUE\')'.format(
                            key))

                if not os.path.isdir(values):
                    raise ValueError('dict_extracted_features_paths[\'{}\'] must be a correct dir'.format(key))

        self.dict_extracted_features_paths = dict_extracted_features_paths

    def create_features_path_link_to(self, result_path, database, type_evaluation):

        basename = os.path.basename(result_path)
        features_paths = self.dict_extracted_features_paths[database.name()][type_evaluation]
        if not self.__check_target_folder(features_paths, basename):
            raise ValueError("{} target folder is not available on "
                             "dict_extracted_features_paths"
                             "[\'{}\'][\'{}\'] = \'{}\'".format(basename,
                                                                database.name(),
                                                                type_evaluation,
                                                                self.dict_extracted_features_paths))

        if database.is_a_collection_of_databases():
            result_path_features = os.path.join(result_path, database.name())
        else:
            result_path_features = os.path.join(result_path)

        if not os.path.isdir(os.path.dirname(result_path_features)):
            os.makedirs(os.path.dirname(result_path_features))

        source_path_features = os.path.join(features_paths, basename)

        symlink_force(source_path_features, result_path_features)

    def __check_target_folder(self, extracted_features_path, basename):
        exist = False
        for basename_dir in os.listdir(extracted_features_path):
            if os.path.isdir(os.path.join(extracted_features_path, basename_dir)):
                if basename == basename_dir:
                    exist = True
                    break
        return exist
