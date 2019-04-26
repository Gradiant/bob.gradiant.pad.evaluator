import logging
import os
import subprocess
import sys
from bob.gradiant.core import FeaturesExtractorManager
from bob.gradiant.core import FeaturesSaver
from bob.gradiant.pipelines import Pipeline, DEFAULT_KEYS_CORRESPONDENCES
from bob.gradiant.core import FeaturesExtractor, AccessGridConfig
from bob.gradiant.face.databases import FaceDatabaseProvider, face_available_databases, export_database_paths_from_file
from bob.gradiant.pad.evaluator.classes.configuration.evaluation_config import evaluation_use_framerate_and_time, \
    evaluation_long_names

try:
    basestring
except NameError:
    basestring = str


class Configuration(object):

    def __init__(self,
                 type_evaluation,
                 database_paths_filename,
                 databases_list,
                 protocols_list,
                 feature_extractor,
                 pipeline,
                 result_path,
                 access_grid_config=AccessGridConfig(),
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
        self.database_paths_filename = database_paths_filename
        self.databases_list = databases_list
        self.protocols_list = protocols_list
        self.feature_extractor = feature_extractor
        self.pipeline = pipeline
        self.result_path = result_path
        self.features_extractor_manager = FeaturesExtractorManager(self.feature_extractor,
                                                                   FeaturesSaver(self.result_path))
        self.access_grid_config = access_grid_config
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
        self.__set_pipeline_key_correspondencies()
        if self.database_paths_filename:
            export_database_paths_from_file(self.database_paths_filename)

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
        _tmp = __import__(basename, globals(), locals(), ['object'])
        database_paths_filename = _tmp.database_paths_filename
        databases_list = _tmp.databases_list
        protocols_list = _tmp.protocols_list
        feature_extractor = _tmp.feature_extractor
        result_path = os.path.join(_tmp.result_path, type_evaluation)
        features_extractor_manager = FeaturesExtractorManager(feature_extractor,
                                                              FeaturesSaver(result_path))

        if type_evaluation == "ACE" or type_evaluation == "AUE":
            pipeline = _tmp.pipeline
            categorized_scores_plotter = _tmp.categorized_scores_plotter

            if evaluation_use_framerate_and_time[type_evaluation]:
                access_grid_config = _tmp.access_grid_config
            else:
                access_grid_config = None

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
        else:  # FE
            pipeline = None
            categorized_scores_plotter = None
            skip_features_extraction = False
            dict_extracted_features_paths = {}
            skip_training = True
            skip_scores_prediction = True
            dict_scores_prediction = {}
            try:
                access_grid_config = _tmp.access_grid_config
            except:
                access_grid_config = None

        verbose = _tmp.verbose
        number_threads = _tmp.number_threads
        use_data_augmentation = _tmp.use_data_augmentation
        recreate = _tmp.recreate

        return cls(type_evaluation,
                   database_paths_filename,
                   databases_list,
                   protocols_list,
                   feature_extractor,
                   pipeline,
                   result_path,
                   access_grid_config=access_grid_config,
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

    def __set_pipeline_key_correspondencies(self):
        if self.pipeline:
            for processor in self.pipeline.processor_list:
                key_correspondencies = DEFAULT_KEYS_CORRESPONDENCES
                key_correspondencies['labels_key'] = 'common_pai'
                processor.key_correspondencies = key_correspondencies

    def __set_git_info(self):
        self.short_commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
        self.repo = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode('utf-8').rsplit('/', 1)[1][:-1]

    def __check_configuration(self):
        logging.info('Checking configuration')

        if self.database_paths_filename:
            if not os.path.isfile(self.database_paths_filename):
                raise IOError("database_paths_filename must be a json file.")

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

        if self.type_evaluation != 'FE':  # Features Extraction
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
            if self.type_evaluation != 'FE':  # Features Extraction
                if not isinstance(self.access_grid_config, AccessGridConfig):
                    raise TypeError(
                        'access_grid_config must be defined as a AccessGridConfig. Please fill it out on \'{}\''.format(
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
            info += attribute.format('access_grid_config -> framerate_list',
                                     self.access_grid_config.framerate_list)
            info += attribute.format('access_grid_config -> total_time_acquisition_list',
                                     self.access_grid_config.total_time_acquisition_list)
            info += attribute.format('access_grid_config -> starting_time_acquisition_list',
                                     self.access_grid_config.starting_time_acquisition_list)
            info += attribute.format('access_grid_config -> center_video_acquisition_list',
                                     self.access_grid_config.center_video_acquisition_list)

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
