#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import logging

from bob.gradiant.pad.evaluator import AlgorithmicConstrainedEvaluationProtocol
from bob.gradiant.pad.evaluator import Configuration
from bob.gradiant.pad.evaluator.classes import evaluator_parser


def main():
    args = evaluator_parser()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    configuration = Configuration.fromfilename('ACE', args.config_file)
    logging.info(configuration)
    configuration.save_to_file()

    algorithmic_constrained_evaluation_protocol = AlgorithmicConstrainedEvaluationProtocol(configuration)
    algorithmic_constrained_evaluation_protocol.run()


if __name__ == '__main__':
    main()
