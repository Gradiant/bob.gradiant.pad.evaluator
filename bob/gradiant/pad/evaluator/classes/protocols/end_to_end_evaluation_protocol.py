#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import time
import cpuinfo
import sys
import os
import pickle
from time import gmtime, strftime
from bob.gradiant.pad.evaluator.classes.configuration.evaluation_config import evaluation_long_names
from bob.gradiant.pad.evaluator.classes.configuration.end_to_end_configuration import EndToEndConfiguration
from bob.gradiant.pad.evaluator.classes.protocols.evaluation_protocol import EvaluationProtocol
from bob.gradiant.core import Informer, Colors, AccessModificator, TypeDatabase, EndToEndTableGenerator, EndToEndInfo

SUBSETS_TO_EVALUATE = ['Test']


def progressBar(value, end_value, name_access, bar_length=20):
    percent = float(value) / end_value
    arrow = '-' * int(round(percent * bar_length) - 1) + '>'
    spaces = ' ' * (bar_length - len(arrow))

    sys.stdout.write("\r\t\tProcessing {0} ({1}/{2}) [{3}]".format(name_access, value, end_value, arrow + spaces))
    sys.stdout.flush()


class EndToEndEvaluationProtocol(EvaluationProtocol):
    parameter_grid = []
    base_path = None

    def __init__(self, configuration):
        if not isinstance(configuration, EndToEndConfiguration):
            raise TypeError("configuration parameter must be a object of EndToEndConfiguration class")

        self.informer = Informer(verbose=configuration.verbose)
        self.configuration = configuration
        super(EndToEndEvaluationProtocol, self).__init__(configuration)

    def run(self, function_to_run='run'):

        for database in self.configuration.databases_list:
            for protocol in self.configuration.protocols_list:
                self.tag_evaluation = '@'.join([database.name(), protocol])
                self.informer.highlight_message(self.tag_evaluation,
                                                title=evaluation_long_names[self.configuration.type_evaluation],
                                                color=Colors.FG.green)

            # Extraction ----------------------------------------------------

            scores_path = os.path.join(self.configuration.result_path, self.tag_evaluation,
                                       self.configuration.face_pad.name, 'scores')
            if not os.path.isdir(scores_path):
                os.makedirs(scores_path)

            scores_filename = os.path.join(scores_path, 'end_to_end_info.h5')

            if not os.path.isfile(scores_filename):
                end_to_end_info = self.__extract_pad_results(scores_filename, database, protocol)
            else:
                self.informer.highlight_message('ok',
                                                title='\tLoading end_to_end_info from \'{}\''.format(scores_filename),
                                                color=Colors.FG.lightgrey)
                end_to_end_info = EndToEndInfo.fromfilename(scores_filename)

            # Evaluation ------------------------------------------------------
            result_path = os.path.join(self.configuration.result_path, self.tag_evaluation,
                                       self.configuration.face_pad.name, 'result')
            self.__evaluation(result_path, end_to_end_info)

    def __extract_pad_results(self, scores_filename, database, protocol):

        self.informer.highlight_message(
            'end-to-end parameters [framerate = {}, total_time_acquisition = {}, threshold = {}]'.format(
                self.configuration.framerate,
                self.configuration.total_time_acquisition,
                self.configuration.threshold),
            title='\tEnd-to-end extraction',
            color=Colors.FG.lightcyan)

        access_modificator = AccessModificator(self.configuration.framerate, self.configuration.total_time_acquisition)

        if database.type_database is TypeDatabase.ALL_FILES_TOGETHER:
            dict_accesses = database.get_accesses_by_subset(access_modificator)
        else:
            dict_accesses = database.get_all_accesses(access_modificator)
        self.informer.set_title('Extracting pad results')
        info = cpuinfo.get_cpu_info()

        name_algorithm = '{}_f{}_ta{}'.format(self.configuration.face_pad.name,
                                              self.configuration.framerate,
                                              self.configuration.total_time_acquisition)
        framerate = self.configuration.framerate
        total_time_of_acquisition = self.configuration.total_time_acquisition
        processor = ' '.join(info['brand'].split())

        processed_frames = 0
        scores_list = []
        time_of_delay_list = []
        cpu_time_list = []
        labels_list = []
        benchmark_labels_list = []

        for subset in SUBSETS_TO_EVALUATE:
            subset_accesses = dict_accesses[subset]
            subset_ground_truth = database.get_ground_truth(protocol)[subset]
            failure_accesses = 0

            for i, access in enumerate(subset_accesses):
                progressBar(i + 1, len(subset_accesses), access.name)
                dict_images = access.load()
                start_time_cpu_processing = time.time() * 1000
                for key, image in dict_images.iteritems():
                    self.configuration.face_pad.process(image)
                    processed_frames += 1
                    if self.configuration.face_pad.is_finished():
                        break
                cpu_time = time.time() * 1000 - start_time_cpu_processing

                start_time_decision = time.time() * 1000
                label, score = self.configuration.face_pad.get_decision()
                time_of_delay = time.time() * 1000 - start_time_decision
                if label == "FAILURE_TO_COMPUTE":
                    failure_accesses += 1
                self.configuration.face_pad.reset()

                scores_list.append(score)
                time_of_delay_list.append(time_of_delay)
                cpu_time_list.append(cpu_time)
                labels_list.append(label)
                benchmark_labels_list += subset_ground_truth

        print '\n\t\tFAILURE_TO_COMPUTE accesses: ' + str(failure_accesses) + '/' + str(len(subset_accesses))

        end_to_end_info = EndToEndInfo(name_algorithm,
                                       framerate,
                                       total_time_of_acquisition,
                                       processor,
                                       processed_frames,
                                       scores_list,
                                       time_of_delay_list,
                                       cpu_time_list,
                                       labels_list,
                                       benchmark_labels_list)
        end_to_end_info.save(scores_filename)
        return end_to_end_info

    def __evaluation(self, result_path, end_to_end_info):

        self.informer.highlight_message(
            'ok',
            title='\tEnd-to-end evaluation',
            color=Colors.FG.lightcyan)

        end_to_end_table_generator = EndToEndTableGenerator(self.tag_evaluation,
                                                            self.configuration.face_pad.name,
                                                            dict(end_to_end_info),
                                                            result_path)
        end_to_end_table_generator.run()
