# -----------------------------------------------------------------
# Configuration file automatically generated at 2018-12-04
# -----------------------------------------------------------------


# REQUIRED ARGUMENTS:

# Database paths:
# * You need to add a json file with the information of the databases
import os
database_paths_filename = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                       'database_paths.json')

# Database and protocol:
from bob.gradiant.pad.evaluator import DummyDatabase

databases_list = [DummyDatabase('resources')]
protocols_list = ['grandtest']

# Feature extraction:
from bob.gradiant.pad.evaluator import DummyFeaturesExtractor

feature_extractor = DummyFeaturesExtractor()

# Result base path:
result_path = 'result'

# Framerate and time parameters:
framerate_list = None
total_time_acquisition_list = None

# -----------------------------------------------------------------

# OPTIONAL ARGUMENTS:

# Verbose (only True/False are valid):
verbose = True

# Number of threads for parallelizing the features extraction:
number_threads = 1

# Data augmentation:
use_data_augmentation = False

# Recreate: If it is true, features extraction will be done overwriting previous files
recreate = False
# -----------------------------------------------------------------
