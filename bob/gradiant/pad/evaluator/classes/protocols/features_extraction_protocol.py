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


class FeaturesExtractionProtocol(EvaluationProtocol):
    parameter_grid = []
    base_path = None

    def __init__(self, configuration):
        if not isinstance(configuration, Configuration):
            raise TypeError("configuration parameter must be a object of Configuration class")

        self.informer = Informer(verbose=configuration.verbose)
        self._set_parameter_grid(configuration)

        self.data_augmentator = DataAugmentator(configuration.use_data_augmentation)
        super(FeaturesExtractionProtocol, self).__init__(configuration)

    def _set_parameter_grid(self, configuration):
        if configuration.access_grid_config:
            self.parameter_grid = configuration.access_grid_config.get_parameter_grid()
        else:
            self.parameter_grid = None

    def run(self):

        for database in self.configuration.databases_list:

            name_experiment = 'experiment'

            experiment_paths = ExperimentPaths(os.path.join(self.configuration.result_path, database.name()),
                                               name_experiment)
            self.informer.highlight_message(database.name(),
                                            title=evaluation_long_names[self.configuration.type_evaluation],
                                            color=Colors.FG.green)
            protocol_utils = ProtocolUtils(self.informer,
                                           self.configuration,
                                           experiment_paths,
                                           name_experiment,
                                           self.data_augmentator)

            # Extraction ----------------------------------------------------

            if self.parameter_grid:
                self.informer.highlight_message(
                    self.configuration.access_grid_config.get_message_summary_parameter_grid(),
                    title=' Extracting features',
                    color=Colors.FG.lightcyan)
                for parameters in self.parameter_grid:
                    self.informer.highlight_message(
                        self.configuration.access_grid_config.get_format_message_from_parameters(parameters),
                        title='  Extracting features',
                        color=Colors.FG.lightgrey)

                    features_path = experiment_paths.get_features_path(parameters)
                    protocol_utils.extract_features(features_path, database, parameters=parameters)
            else:
                self.informer.highlight_message('|',
                                                title=' Extracting features for every frame',
                                                color=Colors.FG.lightcyan)
                features_path = os.path.join(experiment_paths.get_features_path_root(), "whole_video")
                protocol_utils.extract_features(features_path, database)

            # -----------------------------------------------------------------
            self.informer.highlight_message(LINE, title='  ok',
                                            color=Colors.FG.lightcyan)
