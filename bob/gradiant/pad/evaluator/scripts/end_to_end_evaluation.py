#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import logging

from bob.gradiant.pad.evaluator import EndToEndEvaluationProtocol, EndToEndConfiguration
from bob.gradiant.pad.evaluator.classes import evaluator_parser


def main():
    args = evaluator_parser()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    end_to_end_configuration = EndToEndConfiguration.fromfilename(args.config_file)
    logging.info(end_to_end_configuration)
    end_to_end_configuration.save_to_file()

    end_to_end_evaluation_protocol = EndToEndEvaluationProtocol(end_to_end_configuration)
    end_to_end_evaluation_protocol.run()


if __name__ == '__main__':
    main()
