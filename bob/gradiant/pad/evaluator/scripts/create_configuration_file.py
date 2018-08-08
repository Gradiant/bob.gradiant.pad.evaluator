#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import argparse
import logging

from bob.gradiant.pad.evaluator import ConfigurationFileCreator


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-f', '--filename', type=str, dest='filename',
                        help='Creates a configuration file with all necessary values in order to be filled out. '
                             'filename must be a path to a python (.py) file', required=True)
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
    parser.set_defaults(verbose=False)
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    if args.filename is not None:
        ConfigurationFileCreator.run(args.filename)


if __name__ == '__main__':
    main()
