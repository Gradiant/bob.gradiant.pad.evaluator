#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import os
from bob.gradiant.pad.evaluator.classes.utils.extracted_features_manager import ExtractedFeaturesManager
from bob.gradiant.pad.evaluator.classes.configuration.evaluation_config import evaluation_long_names
from bob.gradiant.pad.evaluator.classes.configuration.configuration import Configuration
from bob.gradiant.pad.evaluator.classes.protocols.evaluation_protocol import EvaluationProtocol
from bob.gradiant.pad.evaluator.classes.protocols.experiment_paths import ExperimentPaths
from bob.gradiant.pad.evaluator.classes.protocols.protocol_utils import ProtocolUtils, LINE
from bob.gradiant.core import Informer, DataAugmentator, Colors
from sklearn.model_selection import ParameterGrid


class AlgorithmicConstrainedEvaluationProtocol(EvaluationProtocol):
    parameter_grid = []
    base_path = None

    def __init__(self, configuration):
        if not isinstance(configuration, Configuration):
            raise TypeError("configuration parameter must be a object of Configuration class")

        self.informer = Informer(verbose=configuration.verbose)
        self.parameter_grid = configuration.access_grid_config.get_parameter_grid()
        self.data_augmentator = DataAugmentator(configuration.use_data_augmentation)
        super(AlgorithmicConstrainedEvaluationProtocol, self).__init__(configuration)

    def run(self):

        for database in self.configuration.databases_list:
            self.experiment_paths = ExperimentPaths(os.path.join(self.configuration.result_path, database.name()),
                                                    self.configuration.pipeline.name)
            self.name_experiment = self.configuration.pipeline.name
            self.informer.highlight_message(database.name(),
                                            title=evaluation_long_names[self.configuration.type_evaluation],
                                            color=Colors.FG.green)
            self.protocol_utils = ProtocolUtils(self.informer,
                                                self.configuration,
                                                self.experiment_paths,
                                                self.name_experiment,
                                                self.data_augmentator)

            # Extraction ----------------------------------------------------

            self.informer.highlight_message(self.configuration.access_grid_config.get_message_summary_parameter_grid(),
                                            title=' Extracting features',
                                            color=Colors.FG.lightcyan)

            for parameters in self.parameter_grid:
                self.informer.highlight_message(
                    self.configuration.access_grid_config.get_format_message_from_parameters(parameters),
                    title='  Extracting features',
                    color=Colors.FG.lightgrey)

                features_path = self.experiment_paths.get_features_path(parameters)
                if self.configuration.skip_scores_prediction:
                    self.informer.highlight_message(message='ok',
                                                    title='  Skipping features extraction '
                                                          '(skip_scores_prediction=True)',
                                                    color=Colors.FG.lightred)
                else:
                    if self.configuration.skip_features_extraction:
                        self.informer.highlight_message(message='ok',
                                                        title='  Skipping features extraction '
                                                              '(skip_features_extraction=True)',
                                                        color=Colors.FG.lightred)

                        if self.configuration.dict_extracted_features_paths:
                            extracted_features_manager = ExtractedFeaturesManager(
                                self.configuration.dict_extracted_features_paths)
                            extracted_features_manager.create_features_path_link_to(
                                self.experiment_paths.get_features_path(parameters=parameters), database,
                                self.configuration.type_evaluation)
                        else:
                            raise Warning(
                                'dict_extracted_features_paths configuration '
                                'is not set when skip_features_extraction==True.')
                    else:
                        self.protocol_utils.extract_features(features_path, database, parameters=parameters)

            # -----------------------------------------------------------------
            self.informer.highlight_message(LINE, title='  ok',
                                            color=Colors.FG.lightcyan)

            for protocol in self.configuration.protocols_list:
                if protocol in database.get_protocols():
                    self.informer.highlight_message('',
                                                    title=' Protocol \"{}\"'.format(protocol),
                                                    color=Colors.FG.purple)

                    self.informer.highlight_message(
                        self.configuration.access_grid_config.get_message_summary_parameter_grid(),
                        title='   > Training',
                        color=Colors.FG.lightcyan)

                    for parameters in self.parameter_grid:
                        features_path = self.experiment_paths.get_features_path(parameters)
                        # Training -------------------------------------------------------
                        pipeline_path = self.experiment_paths.get_pipeline_path(protocol, parameters)
                        self.protocol_utils.pipeline(database, protocol, features_path, pipeline_path, parameters)
                        # -----------------------------------------------------------------
                    # Evaluation ------------------------------------------------------
                    self.protocol_utils.evaluation(database, protocol)
                    # -----------------------------------------------------------------
                else:
                    raise Warning(
                        'Skipped \'{}\' protocol. This protocol is not implemented in {} dataset, try with {}'.format(
                            protocol, database.name(), database.get_protocols()))
