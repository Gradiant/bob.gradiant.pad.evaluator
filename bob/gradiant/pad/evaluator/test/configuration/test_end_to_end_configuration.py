#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import unittest
import os
import shutil
from bob.gradiant.pad.evaluator import EndToEndConfiguration
from bob.gradiant.pad.evaluator import DummyFacePad
from bob.gradiant.face.databases import DummyDatabase


class UnitTestEndToEndConfiguration(unittest.TestCase):

    configuration_file = 'resources/config/config_test.py'
    databases = [DummyDatabase('resources')]
    protocols = ['grandtest']
    face_pad = DummyFacePad()
    result_path = 'result'
    framerate = 10
    total_time_acquisition = 500
    verbose = True

    def tearDown(self):
        if os.path.isdir('result'):
            shutil.rmtree('result')

    def test_init_fromfilename_wrong_path(self):
        self.assertRaises(IOError,
                          lambda: EndToEndConfiguration.fromfilename('WRONG')
                          )

    def test_init_fromfilename_correct_params(self):
        EndToEndConfiguration.fromfilename(self.configuration_file)

    def test_init_correct_params_but_database_path_not_defined(self):

        replay_path = None
        if "REPLAY_ATTACK_PATH" in os.environ:
            replay_path =  os.environ["REPLAY_ATTACK_PATH"]
            del os.environ["REPLAY_ATTACK_PATH"]

        self.assertRaises(EnvironmentError,
                          lambda: EndToEndConfiguration('E2E',
                                                ['replay-attack'],
                                                self.protocols,
                                                self.face_pad,
                                                self.result_path,
                                                framerate = self.framerate,
                                                total_time_acquisition = self.total_time_acquisition,
                                                verbose = self.verbose)
                          )

        if replay_path:
            os.environ["REPLAY_ATTACK_PATH"] = replay_path

    def test_init_incorrect_databases_param(self):
        self.assertRaises(TypeError,
                          lambda: EndToEndConfiguration('E2E',
                                                        'WRONG_PARAM',
                                                        self.protocols,
                                                        self.face_pad,
                                                        self.result_path,
                                                        framerate=self.framerate,
                                                        total_time_acquisition=self.total_time_acquisition,
                                                        verbose=self.verbose)
                          )

    def test_init_incorrect_databases_param_no_exist(self):
        self.assertRaises(ValueError,
                          lambda: EndToEndConfiguration('E2E',
                                                        ['no_exist_database'],
                                                        self.protocols,
                                                        self.face_pad,
                                                        self.result_path,
                                                        framerate=self.framerate,
                                                        total_time_acquisition=self.total_time_acquisition,
                                                        verbose=self.verbose)
                          )

    def test_init_incorrect_protocol_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: EndToEndConfiguration('E2E',
                                                        self.databases,
                                                        'WRONG_PARAM',
                                                        self.face_pad,
                                                        self.result_path,
                                                        framerate=self.framerate,
                                                        total_time_acquisition=self.total_time_acquisition,
                                                        verbose=self.verbose)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_incorrect_face_pad_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: EndToEndConfiguration('E2E',
                                                        self.databases,
                                                        self.protocols,
                                                        "WRONG_PARAM",
                                                        self.result_path,
                                                        framerate=self.framerate,
                                                        total_time_acquisition=self.total_time_acquisition,
                                                        verbose=self.verbose)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_none_result_path_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: EndToEndConfiguration('E2E',
                                                        self.databases,
                                                        self.protocols,
                                                        self.face_pad,
                                                        None,
                                                        framerate=self.framerate,
                                                        total_time_acquisition=self.total_time_acquisition,
                                                        verbose=self.verbose)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_incorrect_result_path_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: EndToEndConfiguration('E2E',
                                                        self.databases,
                                                        self.protocols,
                                                        self.face_pad,
                                                        ['WRONG_PARAM'],
                                                        framerate=self.framerate,
                                                        total_time_acquisition=self.total_time_acquisition,
                                                        verbose=self.verbose)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_none_framerate_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: EndToEndConfiguration('E2E',
                                                        self.databases,
                                                        self.protocols,
                                                        self.face_pad,
                                                        self.result_path,
                                                        framerate=None,
                                                        total_time_acquisition=self.total_time_acquisition,
                                                        verbose=self.verbose)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_wrong_framerate_param(self):
        os.environ["REPLAY_ATTACK_PATH"] = "resources"
        self.assertRaises(TypeError,
                          lambda: EndToEndConfiguration('E2E',
                                                        self.databases,
                                                        self.protocols,
                                                        self.face_pad,
                                                        self.result_path,
                                                        framerate='WRONG',
                                                        total_time_acquisition=self.total_time_acquisition,
                                                        verbose=self.verbose)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_none_total_time_acquisition_param(self):
        os.environ["REPLAY_ATTACK_PATH"] = "resources"
        self.assertRaises(TypeError,
                          lambda: EndToEndConfiguration('E2E',
                                                        self.databases,
                                                        self.protocols,
                                                        self.face_pad,
                                                        self.result_path,
                                                        framerate=self.framerate,
                                                        total_time_acquisition=None,
                                                        verbose=self.verbose)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_wrong_total_time_acquisition_param(self):
        os.environ["REPLAY_ATTACK_PATH"] = "resources"
        self.assertRaises(TypeError,
                          lambda: EndToEndConfiguration('E2E',
                                                        self.databases,
                                                        self.protocols,
                                                        self.face_pad,
                                                        self.result_path,
                                                        framerate=self.framerate,
                                                        total_time_acquisition='WRONG',
                                                        verbose=self.verbose)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_none_threshold_param(self):
        os.environ["REPLAY_ATTACK_PATH"] = "resources"
        self.assertRaises(TypeError,
                          lambda: EndToEndConfiguration('E2E',
                                                        self.databases,
                                                        self.protocols,
                                                        self.face_pad,
                                                        self.result_path,
                                                        framerate=self.framerate,
                                                        total_time_acquisition=self.total_time_acquisition,
                                                        threshold=None,
                                                        verbose=self.verbose)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_wrong_threshold_param(self):
        os.environ["REPLAY_ATTACK_PATH"] = "resources"
        self.assertRaises(TypeError,
                          lambda: EndToEndConfiguration('E2E',
                                                        self.databases,
                                                        self.protocols,
                                                        self.face_pad,
                                                        self.result_path,
                                                        framerate=self.framerate,
                                                        total_time_acquisition=self.total_time_acquisition,
                                                        threshold='WRONG',
                                                        verbose=self.verbose)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_none_verbose_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: EndToEndConfiguration('E2E',
                                                        self.databases,
                                                        self.protocols,
                                                        self.face_pad,
                                                        self.result_path,
                                                        framerate=self.framerate,
                                                        total_time_acquisition=self.total_time_acquisition,
                                                        verbose=None)
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_init_wrong_verbose_param(self):
        os.environ["REPLAY_ATTACK_PATH"]="resources"
        self.assertRaises(TypeError,
                          lambda: EndToEndConfiguration('E2E',
                                                        self.databases,
                                                        self.protocols,
                                                        self.face_pad,
                                                        self.result_path,
                                                        framerate=self.framerate,
                                                        total_time_acquisition=self.total_time_acquisition,
                                                        verbose='WRONG')
                          )
        del os.environ["REPLAY_ATTACK_PATH"]

    def test_print_to_file(self):
        filename_result = 'result/configuration.txt'
        configuration = EndToEndConfiguration.fromfilename(self.configuration_file)
        configuration.save_to_file(filename_result)
        self.assertTrue(os.path.isfile(filename_result))





