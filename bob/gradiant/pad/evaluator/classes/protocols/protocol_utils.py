#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import os
import copy
from time import gmtime, strftime
from bob.gradiant.pipelines import ProcessorOutputType
from bob.gradiant.core import PipelineFeaturesFormatLoader, ExperimentResult, Colors, PadEvaluator, PadVisualizationManager, TypeDatabase, AccessModificator, MultiprocessManager
from ..utils.symlink_force import *
SPACES = ' '*80
LINE = '-'*80 + '|'


class ProtocolUtils(object):

    def __init__(self, informer, configuration, experiment_paths, name_experiment, data_augmentator):
        self.informer = informer
        self.experiment_paths = experiment_paths
        self.name_experiment = name_experiment
        self.data_augmentator = data_augmentator
        self.configuration = configuration

    def extract_features(self, features_path, database, function_to_run='run', parameters = None ):
        if parameters:
            access_modificator = AccessModificator(parameters['framerate'], parameters['total_time_acquisition'])
        else:
            access_modificator = AccessModificator()
        if database.type_database is TypeDatabase.ALL_FILES_TOGETHER:
            dict_accesses = database.get_accesses_by_subset(access_modificator)
        else:
            dict_accesses = database.get_all_accesses(access_modificator)

        self.informer.set_title('Extracting features')

        len_total_accesses = 0
        for subset, accesses in dict_accesses.iteritems():
            enable_data_augmentation = False
            if subset is 'Train' and self.configuration.use_data_augmentation:
                enable_data_augmentation = True
            self.__extract_from_accesses(features_path, subset, accesses, data_augmentation=enable_data_augmentation)
            len_total_accesses += len(accesses)
        self.informer.message('Finished. Extracted {} features{}'.format(len_total_accesses, SPACES), color=Colors.FG.green, prefix='\r',suffix='\n')

    def __extract_from_accesses(self, features_path, subset, accesses, data_augmentation = False):

        features_extractor_manager = self.configuration.features_extractor_manager
        multiprocess_manager = MultiprocessManager(self.configuration.number_threads)

        args = []
        counter = 0
        features_extractor_manager.set_base_path(features_path)
        for access in accesses:
            counter += 1
            self.informer = copy.deepcopy(self.informer)
            if data_augmentation:
                text_data_augmentation = ' [data augmentation] '
            else:
                text_data_augmentation=''
            self.informer.set_title('\t\t[ {} ]{} --> {} [ {} | {} ]'.format(subset, text_data_augmentation, access.name, counter, len(accesses)))
            args.append((access, self.informer, self.configuration.recreate, self.data_augmentator))

        multiprocess_manager.run(features_extractor_manager, args)

    ## Pipelines
    def already_exist_experiment_results(self, protocol, subsets, parameters = None):
        exist = True
        for subset in subsets:
            experiment_result_path = self.experiment_paths.get_experiment_result_path(protocol, subset=subset)
            suffix_filename = self.get_experiment_result_filename_from_parameter(parameters)

            filename = os.path.join(experiment_result_path,suffix_filename)
            exist_file = os.path.isfile(filename)
            exist = exist and exist_file
        return exist

    def get_experiment_result_filename_from_parameter(self, parameters = None):
        if parameters:
            suffix_filename = '{}_{}.h5'.format(parameters['framerate'], parameters['total_time_acquisition'])
        else:
            suffix_filename = 'whole_video.h5'
        return suffix_filename

    def read_pipeline_features(self, database, protocol, features_path):
        dict_files_and_labels = database.get_ground_truth(protocol)
        expanded_metadata = self.data_augmentator.get_expanded_metadata(dict_files_and_labels['Train'])
        dict_files_and_labels['Train'] = expanded_metadata

        if database.is_a_collection_of_databases():
            for database_name in database.included_databases.keys():
                features_database_path = os.path.join(features_path, database_name)
                dict_pipeline_features = PipelineFeaturesFormatLoader.run(features_database_path, dict_files_and_labels)
        else:
            dict_pipeline_features = PipelineFeaturesFormatLoader.run(features_path, dict_files_and_labels)
        return dict_pipeline_features

    def save_experiment_result(self, database, Y, protocol, name_pipeline, parameters = None):
        for subset, Y_subset in Y.iteritems():
            experiment_result_path = self.experiment_paths.get_experiment_result_path(protocol,subset = subset)
            suffix_filename = self.get_experiment_result_filename_from_parameter(parameters)
            filename = os.path.join(experiment_result_path,suffix_filename)
            if not self.__exist_experiment_result_file(filename):
                experiment_result = self.__create_experiment_result(database, subset, Y_subset, protocol, name_pipeline, parameters)
                self.experiment_paths.create_dir(experiment_result_path)
                experiment_result.save(filename)

    def __exist_experiment_result_file(self, filename):
        exist = False
        if os.path.isfile(filename):
            exist = True
        return exist

    def __create_experiment_result(self, database, subset, Y, protocol, name_pipeline, parameters = None):

        name_algorithm = self.name_experiment + '_' + protocol + '_' + subset

        if parameters:
            framerate = parameters['framerate']
            total_time_acquisition = parameters['total_time_acquisition']
        else:
            framerate = 30
            total_time_acquisition = -1

        experiment_result = ExperimentResult(name_algorithm,
                                             name_pipeline,
                                             database.name(),
                                             Y['scores'],
                                             Y['labels'],
                                             framerate,
                                             total_time_acquisition,
                                             Y['output_type'] == ProcessorOutputType.DISTANCE,
                                             database.get_attack_dict())

        return experiment_result

    def pipeline(self, database, protocol, features_path, pipeline_path, parameters = None):

        if self.configuration.skip_scores_prediction:
            self.link_scores_prediction(database, protocol, self.configuration.dict_scores_prediction, parameters)
            return

        if parameters:
            self.informer.highlight_message('framerate : {} | total time acquisition : '
                                            '{}'.format(parameters['framerate'], parameters['total_time_acquisition']),
                                            title='\t\tTraining',
                                            color=Colors.FG.lightgrey)
        else:
            self.informer.highlight_message('\'{}\' protocol'.format(protocol),
                                            title='\tPipeline',
                                            color=Colors.FG.lightcyan)

        pipeline = self.configuration.pipeline

        if not self.already_exist_experiment_results(protocol, database.get_subsets(), parameters):
            self.informer.highlight_message(message='ok',
                                            title='\t\tLoading features',
                                            color=Colors.reset)
            X = self.read_pipeline_features(database, protocol, features_path)
            self.informer.highlight_message(message='ok',
                                            title='\t\tLoaded train features ({})'.format(len(X['Train']['features'])),
                                            color=Colors.reset)
            Y = {}
            if self.configuration.skip_training:
                self.informer.highlight_message('Skipping training (skip_training=True)',
                                                title='\tPipeline',
                                                color=Colors.FG.lightcyan)
            else:
                self.informer.highlight_message(message='ok',
                                                title='\t\tTraining {}'.format(pipeline.__str__()),
                                                color=Colors.reset)
                pipeline.fit(X['Train'])

            self.informer.highlight_message(message='ok',
                                            title='\t\tSaving the Pipeline in {}'.format(pipeline_path),
                                            color=Colors.reset)
            pipeline.save(pipeline_path)
            for subset in database.get_subsets():
                self.informer.highlight_message(message='ok',
                                                title='\t\tPredicting scores for {}'.format(subset),
                                                color=Colors.reset)
                Y[subset] = pipeline.run(X[subset])

            self.save_experiment_result(database, Y, protocol, pipeline.__str__(),parameters)
        else:
            self.informer.highlight_message(message='ok',
                                            title='\t\t\tSkipping pipeline. Experiment result already exist',
                                            color=Colors.FG.green)

    def link_scores_prediction(self, database, protocol, dict_scores_prediction, parameters = None):
        self.informer.highlight_message(message='ok',
                                        title='\t\tSkipping pipeline (skip_scores_prediction=True)',
                                        color=Colors.FG.lightred)

        suffix_filename = self.get_experiment_result_filename_from_parameter(parameters)
        for subset in database.get_subsets():
            experiment_result_path = self.experiment_paths.get_experiment_result_path(protocol, subset=subset)
            if not os.path.isdir(experiment_result_path):
                os.makedirs(experiment_result_path)
            source_path_scores = os.path.join(dict_scores_prediction[database.name()][self.configuration.type_evaluation], protocol, subset, suffix_filename)
            symlink_force(source_path_scores,
                          os.path.join(experiment_result_path,
                                       suffix_filename))

    def evaluation(self, database, protocol, subsets):

        self.informer.highlight_message('\'{}\' protocol'.format(protocol), title='\tEvaluation',
                                        color=Colors.FG.lightcyan)

        dict_paths = {}
        for subset in ['Dev', 'Test']:
            experiment_result_path = self.experiment_paths.get_experiment_result_path(protocol, subset=subset)
            dict_paths[subset] = experiment_result_path
        dict_metrics = {'Dev': ['EER'],
                        'Test': ['EER', 'HTER@EER', 'ACER@EER', 'APCER@EER', 'BPCER@EER']
                        }
        dict_performance_visualization = PadEvaluator.run(dict_paths, dict_metrics)

        evaluation_path = self.experiment_paths.get_evaluation_path(protocol)
        self.experiment_paths.create_dir(evaluation_path)
        self.__plot_tables_and_figures(database, protocol, evaluation_path, dict_performance_visualization)

    def __plot_tables_and_figures(self, database, protocol, evaluation_path, dict_performance_visualization):
        date_time = strftime("%Y/%m/%d - %H:%M:%S", gmtime())

        name_database = '@'.join([database.name(), protocol])
        pad_visualization_manager = PadVisualizationManager(name_database,
                                                            self.name_experiment,
                                                            date_time,
                                                            dict_performance_visualization,
                                                            store_path=evaluation_path)
        pad_visualization_manager.plot_fig_pad_time()
        pad_visualization_manager.plot_table()

