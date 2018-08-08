#-----------------------------------------------------------------
# Configuration file automatically generated at 2017-12-13
#-----------------------------------------------------------------


#REQUIRED ARGUMENTS:

#Database and protocol:
from bob.gradiant.pad.evaluator import DummyDatabase
databases_list = [DummyDatabase('resources')]
protocols_list = ['grandtest']

#Feature extraction:
from bob.gradiant.pad.evaluator import DummyFeaturesExtractor
feature_extractor = DummyFeaturesExtractor()

#Pipeline:
from bob.gradiant.pipelines import Pipeline, Pca, LinearSvc
pipeline = Pipeline('test_approach_pca095_linear_svc', [Pca(name='Pca', n_components=0.95), LinearSvc(name='LinearSvc')])

#Result base path:
result_path = 'result'

#Framerate and time parameters:
framerate_list = [15, 20]
total_time_acquisition_list = [1000, 1500]

#-----------------------------------------------------------------

#OPTIONAL ARGUMENTS:

#Verbose (only True/False are valid):
verbose = True

#Number of threads for parallelizing the features extraction:
number_threads = 1

#Data augmentation:
use_data_augmentation = False

#Features extraction:
skip_features_extraction = False
#dict_extracted_features_path = ''

#Training: you can skip training stage
skip_training = False

#Scores prediction:
skip_scores_prediction = False
#dict_scores_paths = ''

#Recreate: If it is true, features extraction will be done overwriting previous files
recreate = False
#-----------------------------------------------------------------

#END-TO-END ARGUMENTS:

#Face-PAD (Presentation Attack Detector):
from bob.gradiant.pad.evaluator import DummyFacePad
face_pad = DummyFacePad()

#Framerate, Fr (end-to-end): optimum value obtained from Algorithmic Constrained Evaluation Protocol
framerate_end_to_end = 15

#Total time of acquisition, Ta (end-to-end): optimum value obtained from Algorithmic Constrained Evaluation Protocol
total_time_acquisition_end_to_end = 500

#Threshold, Th (end-to-end): optimum value obtained from Algorithmic Constrained Evaluation Protocol
threshold_end_to_end = 0.0
#-----------------------------------------------------------------