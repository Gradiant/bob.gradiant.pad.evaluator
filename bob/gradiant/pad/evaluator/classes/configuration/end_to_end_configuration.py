import logging
import os
import subprocess
import sys

from bob.gradiant.pad.evaluator.classes.pad import FacePad
from bob.gradiant.pad.evaluator.classes.configuration.evaluation_config import evaluation_use_framerate_and_time, \
    evaluation_long_names
from bob.gradiant.face.databases import FaceDatabaseProvider, face_available_databases


class EndToEndConfiguration(object):

    def __init__(self,
                 type_evaluation,
                 databases_list,
                 protocols_list,
                 face_pad,
                 result_path,
                 framerate=None,
                 total_time_acquisition=None,
                 threshold = None,
                 verbose=False,
                 configuration_file='\'Configure class\''):

        self.type_evaluation = type_evaluation
        self.databases_list = databases_list
        self.protocols_list = protocols_list
        self.face_pad = face_pad
        self.result_path = result_path
        self.framerate = framerate
        self.total_time_acquisition = total_time_acquisition
        self.threshold = threshold
        self.verbose = verbose
        self.configuration_file = configuration_file
        self.__set_git_info()
        self.__check_configuration()

    @classmethod
    def fromfilename(cls, configuration_file):
        type_evaluation = 'E2E'
        if not os.path.isfile(configuration_file):
            raise IOError("configuration_file ( {} ) does not exist".format(configuration_file))

        logging.info("Reading end-to-end configuration file {}".format(configuration_file))
        dirname = os.path.dirname(configuration_file)
        basename = os.path.splitext(os.path.basename(configuration_file))[0]
        sys.path.append(dirname)
        _tmp = __import__(basename, globals(), locals(), ['object'], -1)
        databases_list = _tmp.databases_list
        protocols_list = _tmp.protocols_list
        face_pad = _tmp.face_pad
        result_path = os.path.join(_tmp.result_path, type_evaluation)
        verbose = _tmp.verbose
        framerate = _tmp.framerate_end_to_end
        total_time_acquisition = _tmp.total_time_acquisition_end_to_end
        threshold = _tmp.threshold_end_to_end

        return cls(type_evaluation,
                   databases_list,
                   protocols_list,
                   face_pad,
                   result_path,
                   framerate=framerate,
                   total_time_acquisition=total_time_acquisition,
                   threshold = threshold,
                   verbose=verbose,
                   configuration_file=configuration_file
                   )

    def __set_git_info(self):
        self.short_commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
        self.repo = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).rsplit('/', 1)[1][:-1]

    def __check_configuration(self):
        logging.info('Checking end-to-end configuration')

        if self.databases_list is None:
            raise TypeError(
                'databases_list is not defined (None Value). Please fill it out on \'{}\''.format(self.configuration_file))
        else:
            if type(self.databases_list) is not list:
                raise TypeError(
                    'databases_list must be defined as a list. Please fill it out on \'{}\''.format(self.configuration_file))
            else:
                self.databases = []
                for key_database in self.databases_list:
                    if isinstance(key_database, basestring):
                        if key_database not in face_available_databases:
                            raise ValueError(
                                '\'{}\' is not one of the implemented databases or the path is not we. Try with: {}'.format(
                                    key_database, face_available_databases))
                        else:
                            database = FaceDatabaseProvider.get(key_database)
                    else:
                        database = key_database
                    self.databases.append(database)

        if self.protocols_list is None:
            raise TypeError(
                'protocols_list is not defined (None Value). Please fill it out on \'{}\''.format(self.configuration_file))
        else:
            if type(self.protocols_list) is not list:
                raise TypeError(
                    'protocols_list must be defined as a list. Please fill it out on \'{}\''.format(self.configuration_file))

        if self.face_pad is None:
            raise TypeError(
                'face_pad is not defined (None Value). Please fill it out on \'{}\''.format(
                    self.configuration_file))
        else:
            if not isinstance(self.face_pad, FacePad):
                raise TypeError(
                    'face_pad must be defined as a bob.gradiant.pad.evaluator.FacePad class. Please fill it out on \'{}\''.format(
                        self.configuration_file))

        if self.result_path is None:
            raise TypeError(
                'result_path is not defined (None Value). Please fill it out on \'{}\''.format(self.configuration_file))

        if not isinstance(self.result_path, basestring):
            raise TypeError(
                'result_path is not defined (None Value). Please fill it out on \'{}\''.format(self.configuration_file))

        if not isinstance(self.verbose, bool):
            raise TypeError(
                'verbose must be a bool value. Please fill it out on \'{}\''.format(
                    self.configuration_file))

        if self.framerate is None:
            raise TypeError(
                'framerate is not defined (None Value). Please fill it out on \'{}\''.format(
                    self.configuration_file))
        else:
            if type(self.framerate) is not int:
                raise TypeError(
                    'framerate must be defined as a int. Please fill it out on \'{}\''.format(
                        self.configuration_file))

        if self.total_time_acquisition is None:
            raise TypeError(
                'total_time_acquisition is not defined (None Value). Please fill it out on \'{}\''.format(
                    self.configuration_file))
        else:
            if type(self.total_time_acquisition) is not int:
                raise TypeError(
                    'total_time_acquisition must be defined as a int. Please fill it out on \'{}\''.format(
                        self.configuration_file))

        if self.threshold is None:
            raise TypeError(
                'threshold is not defined (None Value). Please fill it out on \'{}\''.format(
                    self.configuration_file))
        else:
            if type(self.threshold) is not float:
                raise TypeError(
                    'threshold must be defined as a float. Please fill it out on \'{}\''.format(
                        self.configuration_file))




    def save_to_file(self, filename=None):
        if filename is None:
            filename = os.path.join(self.result_path, 'configuration.txt')
        if not os.path.isdir(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        file = open(filename, "w")
        file.write(self.__str__())
        file.close()

    def __str__(self):
        attribute = '\t\t{} : {}\n'
        info = 'Configuration:\n'
        info += '\tRequired:\n'
        info += attribute.format('type evaluation', evaluation_long_names[self.type_evaluation])
        info += attribute.format('database', self.databases)
        info += attribute.format('protocols', self.protocols_list)
        info += attribute.format('face_pad', self.face_pad)
        info += attribute.format('result_path', self.result_path)
        info += attribute.format('verbose', self.verbose)
        info += attribute.format('framerate', self.framerate)
        info += attribute.format('total_time_acquisition', self.total_time_acquisition)
        info += attribute.format('threshold', self.threshold)

        info += '\tRepository:\n'
        info += attribute.format('name', self.repo)
        info += attribute.format('commit', self.short_commit)
        return info
