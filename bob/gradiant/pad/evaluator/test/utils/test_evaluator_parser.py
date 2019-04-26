#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import unittest
import sys
from bob.gradiant.pad.evaluator import evaluator_parser
from mock import patch

class UnitTestEvaluatorParser(unittest.TestCase):

    def test_evaluator_parser_default(self):
        testargs = ["-r"]
        with patch.object(sys, 'argv', testargs):
            with self.assertRaises(SystemExit):
                args = evaluator_parser()
