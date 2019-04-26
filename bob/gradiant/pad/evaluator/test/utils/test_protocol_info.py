#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import unittest
from bob.gradiant.pad.evaluator import get_protocol_info, save_protocol_info
import numpy as np


class UnitTestProtocolInfo(unittest.TestCase):

    def test_should_return_txt_table(self):
        dict_pipeline_features = {'Train': {'features': np.zeros((1, 10))},
                                  'Dev': {'features': np.zeros((1, 20))},
                                  'Test': {'features': np.zeros((1, 30))}}
        protocol = "Dummy protocol"
        name_db = "Dummy database"

        table_txt = get_protocol_info(dict_pipeline_features, name_db, protocol)
        # save_protocol_info("deleteme.txt", table_txt)
        self.assertTrue(len(table_txt) > 0)
