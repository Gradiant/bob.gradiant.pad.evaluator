# -----------------------------------------------------------------
# Configuration file automatically generated at 2017-12-19
# -----------------------------------------------------------------


# REQUIRED ARGUMENTS:

# Database paths:
# * You need to add a json file with the information of the databases
import os
database_paths_filename = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                       'database_paths.json')

# Database and protocol:
databases_list = ['aggregate-database']
protocols_list = ['grandtest']

# Feature extraction:
from bob.gradiant.pad.evaluator import DummyFeaturesExtractor

feature_extractor = DummyFeaturesExtractor()

# Pipeline:
from bob.gradiant.pipelines import Pipeline, Pca, LinearSvc

pipeline = Pipeline('pipeline_pca095_linear_svc', [Pca(name='Pca', n_components=0.95), LinearSvc(name='LinearSvc')])

# Result base path:
result_path = 'result'

# Framerate and time parameters:
framerate_list = [10, 15]
total_time_acquisition_list = [500, 1000]

# -----------------------------------------------------------------

# OPTIONAL ARGUMENTS:

# Verbose (only True/False are valid):
verbose = True

# Number of threads for parallelizing the features extraction:
number_threads = 1

# Data augmentation:
use_data_augmentation = False

# Features extraction:
skip_features_extraction = False
dict_extracted_features_paths = {'msu-mfsd': '/home/acosta/Software/python/resources/AUE/msu-mfsd/features/',
                                 'replay-attack': '/home/acosta/Software/python/resources/AUE/replay-attack/features/',
                                 'replay-mobile': '/home/acosta/Software/python/resources/AUE/replay-mobile/features/',
                                 'oulu-npu': '/home/acosta/Software/python/resources/AUE/oulu-npu/features/'}

# Training: you can skip training stage
skip_training = False

# Scores prediction:
skip_scores_prediction = False
# dict_scores_paths = ''

# Recreate: If it is true, features extraction will be done overwriting previous files
recreate = False
# -----------------------------------------------------------------

# END-TO-END ARGUMENTS:

# Framerate, Fr (end-to-end): optimum value obtained from Algorithmic Constrained Evaluation Protocol
framerate_end_to_end = None

# Total time of acquisition, Ta (end-to-end): optimum value obtained from Algorithmic Constrained Evaluation Protocol
total_time_acquisition_end_to_end = None
