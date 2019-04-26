#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import os

from bob.gradiant.pad.evaluator.classes.utils.extracted_features_manager import ExtractedFeaturesManager
from bob.gradiant.pad.evaluator.classes.configuration.evaluation_config import evaluation_long_names
from bob.gradiant.pad.evaluator.classes.configuration.configuration import Configuration
from bob.gradiant.pad.evaluator.classes.protocols.evaluation_protocol import EvaluationProtocol
from bob.gradiant.pad.evaluator.classes.protocols.experiment_paths import ExperimentPaths
from bob.gradiant.pad.evaluator.classes.protocols.protocol_utils import ProtocolUtils
from bob.gradiant.core import Informer, DataAugmentator, Colors


class AlgorithmicUnconstrainedEvaluationProtocol(EvaluationProtocol):
    base_path = None

    def __init__(self, configuration):
        if not isinstance(configuration, Configuration):
            raise TypeError("configuration parameter must be a object of Configuration class")

        self.informer = Informer(verbose=configuration.verbose)
        self.data_augmentator = DataAugmentator(configuration.use_data_augmentation)

        super(AlgorithmicUnconstrainedEvaluationProtocol, self).__init__(configuration)

    def run(self):

        for database in self.configuration.databases_list:
            self.experiment_paths = ExperimentPaths(os.path.join(self.configuration.result_path,database.name()),
                                                    self.configuration.pipeline.name)
            self.name_experiment = self.configuration.pipeline.name
            self.protocol_utils = ProtocolUtils(self.informer,
                                                self.configuration,
                                                self.experiment_paths,
                                                self.name_experiment,
                                                self.data_augmentator)
            self.informer.highlight_message(database.name(),
                                            title=evaluation_long_names[self.configuration.type_evaluation],
                                            color=Colors.FG.green)

            # Extraction ----------------------------------------------------
            features_path = self.experiment_paths.get_features_path()
            if self.configuration.skip_scores_prediction:
                self.informer.highlight_message(message='ok',
                                                title='  Skipping features extraction (skip_scores_prediction=True)',
                                                color=Colors.FG.lightred)
            else:
                if self.configuration.skip_features_extraction:
                    self.informer.highlight_message(message='ok',
                                                    title='  Skipping features extraction '
                                                          '(skip_features_extraction=True)',
                                                    color=Colors.FG.lightred)

                    if self.configuration.dict_extracted_features_paths:
                        extracted_features_manager = ExtractedFeaturesManager(self.configuration.dict_extracted_features_paths)
                        extracted_features_manager.create_features_path_link_to(self.experiment_paths.get_features_path(), database, self.configuration.type_evaluation)
                    else:
                        raise Warning('dict_extracted_features_paths configuration '
                                      'is not set when skip_features_extraction==True.')
                else:
                    self.informer.highlight_message('Using whole video and all frames',
                                                    title=' Extracting features',
                                                    color=Colors.FG.lightcyan)
                    self.protocol_utils.extract_features(features_path, database)
            # -----------------------------------------------------------------

            for protocol in self.configuration.protocols_list:
                if protocol in database.get_protocols():
                    # Training -------------------------------------------------------
                    pipeline_path = self.experiment_paths.get_pipeline_path(protocol)
                    self.protocol_utils.pipeline(database, protocol, features_path, pipeline_path)
                    # -----------------------------------------------------------------

                    # Evaluation ------------------------------------------------------
                    self.protocol_utils.evaluation(database, protocol)
                    # -----------------------------------------------------------------
                else:
                    raise Warning('Skipped \'{}\' protocol. T'
                                  'his protocol is not implemented in {} dataset, '
                                  'try with {}'.format(protocol,
                                                       database.name(),
                                                       database.get_subsets()))
