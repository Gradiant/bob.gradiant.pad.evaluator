# bob.gradiant.pad.evaluator 

[Bob](https://www.idiap.ch/software/bob/) package with several scripts to launch experiments aimed at the field of anti-spoofing. 
Several of these scripts take real-world parameters (framerate, acquisition time, etc.) into account, so they allow us to bring several perspectives to our evaluation.

## Environment

We strongly recommend to use [conda](https://conda.io/docs/) to manage the project environment.

There is available two shared recipes to create the enviroment for this project on anaconda cloud.

*Linux*
~~~
conda env create gradiant/biometrics_py27
~~~

*Mac Os*
~~~
conda env create gradiant/biometrics_mac_py27
~~~

If you prefer to install the environment from yaml files:

*Linux*
~~~
conda env create -f environments/biometrics_ubuntu_py27.yml
~~~

*Mac Os*
~~~
conda env create -f environments/biometrics_mac_py27.yml
~~~

## Installation

We assume you have activate biometrics_py27 (or biometrics_mac_py27) environment 

~~~
source activate biometrics_py27
~~~

Then, you can buildout the project with:

~~~
  cd bob.gradiant.pad.evaluator
  python bootstrap-buildout.py
  bin/buildout
~~~

## Test

~~~
  bin/nosetests -v
~~~


## Clean

~~~
  python clean.py
~~~

## Coverage

~~~  
  bin/coverage run -m unittest discover
  bin/coverage html -i
  bin/coverage xml -i
~~~

Coverage result will be store on htmlcov/.

## Doc

~~~
bin/sphinx-build -b html doc/ doc/html/
~~~


## Console scripts

~~~
  bin/create_configuration_file.py
  bin/algorithmic_constrained_evaluation.py
  bin/algorithmic_unconstrained_evaluation.py
  bin/end2end_evaluation.py
~~~


## How to use it


First of all, we should create a configuration file:
```
bin/create_configuration_file.py -f config/config_experiment_1.py
```

Once, the configuration file is created, you have to fill it out. The following values are mandatories:
* databases: 
    * Can be a list of keys for implemented databases, ```databases = ['replay', 'replaymobile', 'msu-mfsd', 'oulu-npu']```
    * Can be also a list of bob.gradiant.core.Database objects, ```database = [ MyDatabaseWhichMetWithTheInterface()] ```
    * Can be a combination of two last, ```databases = ['replay', MyDatabaseWhichMetWithTheInterface()] ```
* protocols:
    * It must be a list of strings. For now about available protocols see bob.gradiant.core, e.g ``` protocols = ['grandtest'] ```
* extraction:
    * It must be an inherit object from bob.gradiant.core.FeatureExtractor
    * You can also define your own feature_extraction object as long as it met the bob.gradiant.core.FeatureExtractor interface, ```feature_extractor = DummyFeaturesExtractor() ```
* pipelines:
    * It must be an inherit object from bob.gradiant.pipelines.Pipeline
    * You can also define your own pipeline object as long as it met the bob.gradiant.pipelines.Pipeline interface, ```pipeline = Pipeline('test_approach_pca095_linear_svc', [Pca(name='Pca', n_components=0.95), LinearSvc(name='LinearSvc')]) ```
* result_path:
    * where we want to save all the results
* Framerate and time parameters (only for ACE):
    * framerate_list: framerates list to evaluate, ````framerate_list = [5, 10, 15, 20, 25]````
    * total_time_acquisition_list: time acquisition list to evaluate, ````total_time_acquisition_list = [500, 1000, 1500, 2000]````


Once we have filled in all the fields, we can run three kind of evaluation experiments.


*AUE - Algorithmic Unconstrained Evaluation*

```
bin/algorithmic_unconstrained_evaluation.py -r config/config_experiment_1.py
```

*ACE - Algorithmic Constrained Evaluation*

```
bin/algorithmic_unconstrained_evaluation.py -r config/config_experiment_1.py
```


*E2E - End-to-end Evaluation*

```
bin/end2end_evaluation.py -r config/config_experiment_1.py
```