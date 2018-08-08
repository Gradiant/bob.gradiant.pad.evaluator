#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import logging

from bob.gradiant.pad.evaluator import Configuration
from bob.gradiant.pad.evaluator.classes import evaluator_parser
from bob.gradiant.pad.evaluator import AlgorithmicUnconstrainedEvaluationProtocol


def main():
    args = evaluator_parser()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    configuration = Configuration.fromfilename('AUE', args.config_file)

    logging.info(configuration)
    configuration.save_to_file()

    algorithmic_unconstrained_evaluation_protocol = AlgorithmicUnconstrainedEvaluationProtocol(configuration)
    algorithmic_unconstrained_evaluation_protocol.run()


if __name__ == '__main__':
    main()