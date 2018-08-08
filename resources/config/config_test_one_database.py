#-----------------------------------------------------------------
# Configuration file automatically generated at 2017-12-19
#-----------------------------------------------------------------


#REQUIRED ARGUMENTS:

#Database and protocol:
databases_list = ['msu-mfsd']
protocols_list = ['grandtest']

#Feature extraction:
from bob.gradiant.pad.evaluator import DummyFeaturesExtractor
feature_extractor = DummyFeaturesExtractor()

#Pipeline:
from bob.gradiant.pipelines import Pipeline, Pca, LinearSvc
pipeline = Pipeline('pipeline_pca095_linear_svc', [Pca(name='Pca', n_components=0.95), LinearSvc(name='LinearSvc')])

#Result base path:
result_path = 'result'

#Framerate and time parameters:
framerate_list = [10, 15]
total_time_acquisition_list = [500, 1000]

#-----------------------------------------------------------------

#OPTIONAL ARGUMENTS:

#Verbose (only True/False are valid):
verbose = True

#Number of threads for parallelizing the features extraction:
number_threads = 20

#Data augmentation:
use_data_augmentation = False

#Features extraction:
skip_features_extraction = False
dict_extracted_features_paths = {'msu-mfsd': '/home/acosta/Software/python/resources/AUE/msu-mfsd/features/'}
#dict_extracted_features_paths = {'msu-mfsd': '/home/acosta/Software/python/resources/ACE/msu-mfsd/features'}

#Training: you can skip training stage
skip_training = False

#Scores prediction:
skip_scores_prediction = False
#dict_scores_paths = ''

#Recreate: If it is true, features extraction will be done overwriting previous files
recreate = False
#-----------------------------------------------------------------

#END-TO-END ARGUMENTS:

#Framerate, Fr (end-to-end): optimum value obtained from Algorithmic Constrained Evaluation Protocol
framerate_end_to_end = None

#Total time of acquisition, Ta (end-to-end): optimum value obtained from Algorithmic Constrained Evaluation Protocol
total_time_acquisition_end_to_end = None

#Threshold, Th (end-to-end): optimum value obtained from Algorithmic Constrained Evaluation Protocol
threshold_end_to_end = None
#-----------------------------------------------------------------