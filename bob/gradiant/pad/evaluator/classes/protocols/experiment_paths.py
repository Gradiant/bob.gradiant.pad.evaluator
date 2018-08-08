#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import os


class ExperimentPaths(object):
    parameter_format = 'framerate{}_time_capture{}'

    def __init__(self, base_path, name_pipeline):
        self.experiment_path = base_path
        self.name_pipeline = name_pipeline

    def get_features_path(self, parameters = None):
        if parameters:
            last_folder = self.parameter_format.format(parameters['framerate'],parameters['total_time_acquisition'])
        else:
            last_folder = 'whole_video'
        return os.path.join(self.experiment_path, 'features',last_folder)

    def get_features_path_root(self):
        return os.path.join(self.experiment_path, 'features')

    def get_scores_path(self, parameters = None):
        if parameters:
            last_folder = self.parameter_format.format(parameters['framerate'],parameters['total_time_acquisition'])
        else:
            last_folder = 'whole_video'
        return os.path.join(self.experiment_path, 'end2end', 'scores', last_folder)

    def get_scores_path_root(self):
        return os.path.join(self.experiment_path,'end2end', 'scores')

    def get_pipeline_path(self, protocol, parameters = None):
        if parameters:
            last_folder = self.parameter_format.format(parameters['framerate'], parameters['total_time_acquisition'])
        else:
            last_folder = 'whole_video'
        return os.path.join(self.experiment_path,'pipelines', self.name_pipeline, 'configurations', protocol,last_folder)

    def get_experiment_result_path(self, protocol, subset = ''):
        return  os.path.join(self.experiment_path,'pipelines', self.name_pipeline, 'experiment_result', protocol, subset)

    def get_evaluation_path(self, protocol):
        return os.path.join(self.experiment_path,'pipelines', self.name_pipeline, 'evaluation', protocol)

    def create_dir(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)

    def create_link(self, src, dst):
        os.symlink(src, dst)
