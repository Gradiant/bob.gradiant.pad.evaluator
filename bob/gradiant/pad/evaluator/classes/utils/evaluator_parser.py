#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import argparse

def evaluator_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-r', '--run', type=str, dest='config_file',
                        help='Run the experiment using given a config_file. '
                             'This configuration file must contain one or more of "databases", "pipelines", '
                             '"features_extractor", and/or some experiment settings', required = True)
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    parser.set_defaults(verbose=False)
    args = parser.parse_args()
    return args
