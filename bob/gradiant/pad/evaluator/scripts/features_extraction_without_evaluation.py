#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2019+ Gradiant, Vigo, Spain
import logging

from bob.gradiant.pad.evaluator import FeaturesExtractionProtocol
from bob.gradiant.pad.evaluator import Configuration
from bob.gradiant.pad.evaluator.classes import evaluator_parser


def main():
    args = evaluator_parser()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    configuration = Configuration.fromfilename('FE', args.config_file)
    logging.info(configuration)
    configuration.save_to_file()

    features_extraction_protocol = FeaturesExtractionProtocol(configuration)
    features_extraction_protocol.run()


if __name__ == '__main__':
    main()
