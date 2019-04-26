1  # !/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
from bob.gradiant.face.databases import face_available_databases

line = '# -----------------------------------------------------------------\n'


def get_required_arguments():
    required = "# REQUIRED ARGUMENTS:\n\n"
    required += "# Database paths:\n"
    required += "# * You need to add a json file with the information of the databases\n"
    required += "database_paths_filename = None\n\n"
    required += "# Database and protocol:\n"
    required += "# * registered databases are: {}\n".format(face_available_databases)
    required += "# * registered protocols are multiples and you need to check each database, here we leave some common examples: ['grandtest', 'print', 'replay']\n"
    required += "# * note that you can select several databases or protocols to fill the list out (e.g databases_list = ['replay-mobile', 'oulu-npu']; protocols_list = ['grandtest'])\n"
    required += "# * you can define your own database object as long as it met the bob.gradiant.core.Database interface\n"
    required += "# * you can use on the same list labels (e.g 'replay-attack', 'replay-mobile', etc) and bob.gradiant.core.Database classes. e.g databases_list = [ MyDatabase('path/to/database'), 'replay-mobile']\n"
    required += "# * databases paths must be defined as a environment variables. (REPLAY_ATTACK_PATH, REPLAY_MOBILE_PATH, MSU_MFSD_PATH, OULU_NPU_PATH) \n"
    required += "# os.environ[\'REPLAY_ATTACK_PATH\'] = \'<path-to-database>\' (if not defined)\n"
    required += "# os.environ[\'REPLAY_MOBILE_PATH\'] = \'<path-to-database>\' (if not defined)\n"
    required += "# os.environ[\'MSU_MFSD_PATH\'] = \'<path-to-database>\' (if not defined)\n"
    required += "# os.environ[\'OULU_NPU_PATH\'] = \'<path-to-database>\' (if not defined)\n"
    required += "databases_list = None\n"
    required += "protocols_list = None\n"
    required += '\n'
    required += "# Feature extraction:\n"
    required += "# You can define your own feature_extraction object as long as it met the bob.gradiant.core.FeatureExtractor interface\n"
    required += "# Example:\n"
    required += "# from bob.gradiant.pad.evaluator import DummyFeaturesExtractor\n"
    required += "# feature_extractor = DummyFeaturesExtractor()\n"
    required += "feature_extractor = None\n"
    required += '\n'
    required += "# Pipeline:\n"
    required += "# You can define your own pipeline object as long as it met the bob.gradiant.pipelines.Pipeline interface\n"
    required += "# Example:\n"
    required += "# from bob.gradiant.pipelines import Pipeline, Pca, LinearSvc\n"
    required += "# pipeline = Pipeline('test_approach_pca095_linear_svc', [Pca(name='Pca', n_components=0.95),\n"
    required += "#                                                         LinearSvc(name='LinearSvc')])\n"
    required += "pipeline = None\n\n"
    required += "# Result base path:\n"
    required += "result_path = None\n\n"
    required += "# Framerate and time parameters:\n"
    required += "# * Ignore these if you are not benchmarking your system with ACE (Algorithmic Contrained Evaluation)\n"
    required += "# * framerate_list : framerates list to evaluate (e.g [5, 10, 15, 20, 25] in FPS)\n"
    required += "# * total_time_acquisition_list : framerates list to evaluate (e.g [500, 1000, 1500, 2000] in milliseconds)\n"
    required += "# * starting_time_acquisition_list : a list with selected points to start the video. Frames before this value will be discarded. (e.g [500, 1000, 1500, 2000] in milliseconds)\n"
    required += "# * center_video_acquisition_list : Bool value. If True, it will ignore the starting_time value and crop the video from the central point.\n"
    required += "from bob.gradiant.core import AccessGridConfig\n"
    required += "access_grid_config = AccessGridConfig(framerate_list=[15, 20], total_time_acquisition_list=[1000, 1500], starting_time_acquisition_list=[100], center_video_acquisition_list=[False])\n\n"
    return required


def get_optional_arguments():
    optional = "# OPTIONAL ARGUMENTS:\n\n"
    optional += "# Verbose (two levels available: True or False):\n"
    optional += "verbose = True\n\n"
    optional += "# Number of threads for parallelizing the features extraction:\n"
    optional += "number_threads = 1\n\n"
    optional += "# Data augmentation:\n"
    optional += "use_data_augmentation = False\n\n"
    optional += "# Features extraction: you can skip extraction stage if you have already extracted your features\n"
    optional += "# * if you set skip_features_extraction to True, you must set the dict_extracted_features_paths\n"
    optional += "# * dict_extracted_features_paths = {'name-database', <path-to-features>}\n"
    optional += "skip_features_extraction = False\n"
    optional += "#dict_extracted_features_paths = None\n\n"
    optional += "#Training: you can skip training stage\n"
    optional += "skip_training = False\n\n"
    optional += "# Scores prediction: you can skip scores prediction if you have already available the scores\n"
    optional += "# * if you set skip_scores_prediction to True, you must set the dict_scores_paths\n"
    optional += "# * dict_scores_paths = {'name-database', <path-to-scores>}\n"
    optional += "skip_scores_prediction = False\n"
    optional += "#dict_scores_paths = None\n\n"
    optional += "# Recreate: If it is true, features extraction will be done overwriting previous files\n"
    optional += "recreate = False\n"
    return optional


def get_end_to_end_arguments():
    end_to_end = "# END-TO-END ARGUMENTS:\n\n"
    end_to_end += "# Face-PAD (Presentation Attack Detector): \n"
    end_to_end += "# You can define your own facePad object as long as it met the bob.gradiant.core.FacePad interface\n"
    end_to_end += "# Example:\n"
    end_to_end += "# from bob.gradiant.pad.evaluator import DummyFacePad\n"
    end_to_end += "# face_pad = DummyFacePad( threshold = 0.0)\n"
    end_to_end += "face_pad = None\n"
    end_to_end += "# Framerate, Fr (end-to-end): optimum value obtained (int) from Algorithmic Constrained Evaluation Protocol\n"
    end_to_end += "framerate_end_to_end = None\n\n"
    end_to_end += "# Total time of acquisition, Ta (end-to-end): optimum value (int) obtained from Algorithmic Constrained Evaluation Protocol\n"
    end_to_end += "total_time_acquisition_end_to_end = None\n\n"
    return end_to_end
