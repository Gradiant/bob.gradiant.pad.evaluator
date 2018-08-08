import logging
import os
import subprocess
import sys
from bob.gradiant.core import FeaturesExtractorManager
from bob.gradiant.core import FeaturesSaver
from bob.gradiant.pipelines import Pipeline
from bob.gradiant.core import FeaturesExtractor
from bob.gradiant.face.databases import FaceDatabaseProvider, face_available_databases
from bob.gradiant.pad.evaluator.classes.configuration.evaluation_config import evaluation_use_framerate_and_time, \
    evaluation_long_names


class Configuration(object):

    def __init__(self, type_evaluation,
                 databases_list,
                 protocols_list,
                 feature_extractor,
                 pipeline,
                 result_path,
                 framerate_list=None,
                 total_time_acquisition_list=None,
                 verbose=False,
                 number_threads=1,
                 use_data_augmentation=False,
                 skip_features_extraction=False,
                 dict_extracted_features_paths=None,
                 skip_training=False,
                 skip_scores_prediction=False,
                 dict_scores_prediction=None,
                 recreate=False,
                 configuration_file='\'Configure class\''):
        if type_evaluation not in evaluation_long_names.keys():
            raise ValueError("type_evaluation is not available. Try with {}".format(evaluation_long_names.keys()))

        self.type_evaluation = type_evaluation
        self.databases_list = databases_list
        self.protocols_list = protocols_list
        self.feature_extractor = feature_extractor
        self.pipeline = pipeline
        self.result_path = result_path
        self.features_extractor_manager = FeaturesExtractorManager(self.feature_extractor,
                                                                   FeaturesSaver(self.result_path))
        self.framerate_list = framerate_list
        self.total_time_acquisition_list = total_time_acquisition_list
        self.verbose = verbose
        self.number_threads = number_threads
        self.use_data_augmentation = use_data_augmentation
        self.skip_features_extraction = skip_features_extraction
        self.dict_extracted_features_paths = dict_extracted_features_paths
        self.skip_training = skip_training
        self.skip_scores_prediction = skip_scores_prediction
        self.dict_scores_prediction = dict_scores_prediction
        self.recreate = recreate
        self.configuration_file = configuration_file
        self.__set_git_info()
        self.__check_configuration()

    @classmethod
    def fromfilename(cls, type_evaluation, configuration_file):
        if not os.path.isfile(configuration_file):
            raise IOError("configuration_file ( {} ) does not exist".format(configuration_file))

        if type_evaluation not in evaluation_long_names.keys():
            raise ValueError("type_evaluation is not available. Try with {}".format(evaluation_long_names.keys()))

        logging.info("Reading configuration file {}".format(configuration_file))
        dirname = os.path.dirname(configuration_file)
        basename = os.path.splitext(os.path.basename(configuration_file))[0]
        sys.path.append(dirname)
        _tmp = __import__(basename, globals(), locals(), ['object'], -1)
        databases_list = _tmp.databases_list
        protocols_list = _tmp.protocols_list
        feature_extractor = _tmp.feature_extractor
        pipeline = _tmp.pipeline
        result_path = os.path.join(_tmp.result_path, type_evaluation)
        features_extractor_manager = FeaturesExtractorManager(feature_extractor,
                                                              FeaturesSaver(result_path))
        if evaluation_use_framerate_and_time[type_evaluation]:
            framerate_list = _tmp.framerate_list
            total_time_acquisition_list = _tmp.total_time_acquisition_list
        else:
            framerate_list = None
            total_time_acquisition_list = None
        verbose = _tmp.verbose
        number_threads = _tmp.number_threads
        use_data_augmentation = _tmp.use_data_augmentation
        skip_features_extraction = _tmp.skip_features_extraction
        if hasattr(_tmp, 'dict_extracted_features_paths'):
            dict_extracted_features_paths = _tmp.dict_extracted_features_paths
        else:
            dict_extracted_features_paths = None
        skip_training = _tmp.skip_training
        skip_scores_prediction = _tmp.skip_scores_prediction
        if hasattr(_tmp, 'dict_scores_prediction'):
            dict_scores_prediction = _tmp.dict_scores_prediction
        else:
            dict_scores_prediction = None

        recreate = _tmp.recreate
        return cls(type_evaluation,
                   databases_list,
                   protocols_list,
                   feature_extractor,
                   pipeline,
                   result_path,
                   framerate_list=framerate_list,
                   total_time_acquisition_list=total_time_acquisition_list,
                   verbose=verbose,
                   number_threads=number_threads,
                   use_data_augmentation=use_data_augmentation,
                   skip_features_extraction=skip_features_extraction,
                   dict_extracted_features_paths=dict_extracted_features_paths,
                   skip_training=skip_training,
                   recreate=recreate,
                   skip_scores_prediction=skip_scores_prediction,
                   dict_scores_prediction=dict_scores_prediction,
                   configuration_file=configuration_file
                   )

    def __set_git_info(self):
        self.short_commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
        self.repo = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).rsplit('/', 1)[1][:-1]

    def __check_configuration(self):
        logging.info('Checking configuration')

        if self.databases_list is None:
            raise TypeError('databases_list is not defined (None Value). '
                            'Please fill it out on \'{}\''.format(self.configuration_file))
        else:
            if type(self.databases_list) is not list:
                raise TypeError('databases_list must be defined as a list. '
                                'Please fill it out on \'{}\''.format(self.configuration_file))
            else:
                databases_list_objects = []
                for key_database in self.databases_list:
                    if isinstance(key_database, basestring):
                        if key_database not in face_available_databases:
                            raise ValueError('\'{}\' is not one of the implemented databases or the path is not we. '
                                             'Try with: {}'.format(key_database, face_available_databases))
                        else:
                            database = FaceDatabaseProvider.get(key_database)
                    else:
                        database = key_database
                    databases_list_objects.append(database)
                self.databases_list = databases_list_objects

        if self.protocols_list is None:
            raise TypeError('protocols_list is not defined (None Value). '
                            'Please fill it out on \'{}\''.format(self.configuration_file))
        else:
            if type(self.protocols_list) is not list:
                raise TypeError(
                    'protocols must be defined as a list. Please fill it out on \'{}\''.format(self.configuration_file))

        if self.feature_extractor is None:
            raise TypeError(
                'protocols_list is not defined (None Value). Please fill it out on \'{}\''.format(
                    self.configuration_file))
        else:
            if not isinstance(self.feature_extractor, FeaturesExtractor):
                raise TypeError('feature_extractor must be defined as a bob.gradiant.core.FeaturesExtractor class. '
                                'Please fill it out on \'{}\''.format(self.configuration_file))

        if self.features_extractor_manager is None:
            raise TypeError('features_extractor_manager is not defined (None Value). '
                            'Please fill feature_extractor and result_path out on \'{}\''
                            .format(self.configuration_file))
        else:
            if not isinstance(self.features_extractor_manager, FeaturesExtractorManager):
                raise TypeError(
                    'features_extractor_manager must be defined as a bob.gradiant.core.FeaturesExtractorManager class. '
                    'Please fill feature_extractor and result_path out on \'{}\''.format(
                        self.configuration_file))

        if self.pipeline is None:
            raise TypeError(
                'pipeline is not defined (None Value). Please fill it out on \'{}\''.format(self.configuration_file))
        else:
            if not isinstance(self.pipeline, Pipeline):
                raise TypeError(
                    'pipeline must be defined as a bob.gradiant.pipeline.Pipelines class. Please fill it out on \'{}\''.format(
                        self.configuration_file))

        if self.result_path is None:
            raise TypeError(
                'result_path is not defined (None Value). Please fill it out on \'{}\''.format(self.configuration_file))

        if not isinstance(self.result_path, basestring):
            raise TypeError(
                'result_path is not defined (None Value). Please fill it out on \'{}\''.format(self.configuration_file))

        if evaluation_use_framerate_and_time[self.type_evaluation]:
            if self.framerate_list is None:
                raise TypeError(
                    'framerate_list is not defined (None Value). Please fill it out on \'{}\''.format(
                        self.configuration_file))
            else:
                if type(self.framerate_list) is not list:
                    raise TypeError(
                        'framerate_list must be defined as a list. Please fill it out on \'{}\''.format(
                            self.configuration_file))
            if self.total_time_acquisition_list is None:
                raise TypeError(
                    'total_time_acquisition_list is not defined (None Value). Please fill it out on \'{}\''.format(
                        self.configuration_file))
            else:
                if type(self.total_time_acquisition_list) is not list:
                    raise TypeError(
                        'total_time_acquisition_list must be defined as a list. Please fill it out on \'{}\''.format(
                            self.configuration_file))

        if not isinstance(self.verbose, bool):
            raise TypeError(
                'verbose must be a bool value. Please fill it out on \'{}\''.format(
                    self.configuration_file))

        if not isinstance(self.number_threads, int):
            raise TypeError(
                'number_threads must be a int value. Please fill it out on \'{}\''.format(
                    self.configuration_file))

        if not isinstance(self.use_data_augmentation, bool):
            raise TypeError(
                'use_data_augmentation must be a bool value. Please fill it out on \'{}\''.format(
                    self.configuration_file))

        if not isinstance(self.skip_features_extraction, bool):
            raise TypeError(
                'skip_features_extraction must be a bool value. Please fill it out on \'{}\''.format(
                    self.configuration_file))

        if self.skip_features_extraction:
            if not isinstance(self.dict_extracted_features_paths, dict):
                raise TypeError(
                    'dict_extracted_features_paths must be a dict. key = Database.name, value = <path-to-features-folder>. Please fill it out on \'{}\''.format(
                        self.configuration_file))

        if not isinstance(self.skip_training, bool):
            raise TypeError(
                'skip_training must be a bool value. Please fill it out on \'{}\''.format(
                    self.configuration_file))

        if not isinstance(self.skip_scores_prediction, bool):
            raise TypeError(
                'skip_scores_prediction must be a bool value. Please fill it out on \'{}\''.format(
                    self.configuration_file))

        if self.skip_scores_prediction:
            if not isinstance(self.dict_scores_prediction, dict):
                raise TypeError(
                    'dict_scores_prediction must be a dict. key = Database.name, value = <path-to-scores-folder>. Please fill it out on \'{}\''.format(
                        self.configuration_file))

        if not isinstance(self.recreate, bool):
            raise TypeError(
                'recreate must be a bool value. Please fill it out on \'{}\''.format(
                    self.configuration_file))

    def save_to_file(self, filename=None):
        if filename is None:
            filename = os.path.join(self.result_path, 'configuration.txt')
        if not os.path.isdir(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        file = open(filename, "w")
        file.write(self.__str__())
        file.close()

    def __str__(self):
        attribute = '\t\t{} : {}\n'
        info = 'Configuration:\n'
        info += '\tRequired:\n'
        info += attribute.format('type evaluation', evaluation_long_names[self.type_evaluation])
        if evaluation_use_framerate_and_time[self.type_evaluation]:
            info += attribute.format('framerate_list', self.framerate_list)
            info += attribute.format('total_time_acquisition_list', self.total_time_acquisition_list)
        info += attribute.format('database_list', self.databases_list)
        info += attribute.format('protocols_list', self.protocols_list)
        info += attribute.format('feature_extractor', self.feature_extractor)
        info += attribute.format('feature_extractor_manager', self.features_extractor_manager)
        info += attribute.format('pipeline', self.pipeline)
        info += attribute.format('result_path', self.result_path)
        info += '\tOptional:\n'
        info += attribute.format('verbose', self.verbose)
        info += attribute.format('number_threads', self.number_threads)
        info += attribute.format('use_data_augmentation', self.use_data_augmentation)
        info += attribute.format('skip_features_extraction', self.skip_features_extraction)
        info += attribute.format('dict_extracted_features_paths', self.dict_extracted_features_paths)
        info += attribute.format('skip_training', self.skip_training)
        info += attribute.format('skip_scores_prediction', self.skip_scores_prediction)
        info += attribute.format('dict_scores_prediction', self.dict_scores_prediction)
        info += attribute.format('recreate', self.recreate)
        info += '\tRepository:\n'
        info += attribute.format('name', self.repo)
        info += attribute.format('commit', self.short_commit)
        return info
