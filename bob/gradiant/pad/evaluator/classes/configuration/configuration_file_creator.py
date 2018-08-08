import datetime
import logging
import os
from bob.gradiant.pad.evaluator.classes.utils.arguments_manager import *


class ConfigurationFileCreator():

    def __init__(self):
        pass

    @staticmethod
    def run(path):
        logging.info('Creating configuration file {}'.format(path))
        dirname = os.path.dirname(path)

        if not os.path.isdir(dirname) and not dirname == "":
            os.makedirs(dirname)

        if '.py' not in os.path.basename(path):
            raise ValueError('{} must be a path to a python (.py) file'.format(path))

        header = '# Configuration file automatically generated at {}\n'.format(datetime.date.today())
        required = get_required_arguments()
        optional = get_optional_arguments()
        end_to_end = get_end_to_end_arguments()
        with open(path, 'w') as f:
            f.write(line)
            f.write(header)
            f.write(line + '\n\n')
            f.write(required)
            f.write(line + '\n')
            f.write(optional)
            f.write(line + '\n')
            f.write(end_to_end)
            f.write(line)
        f.close()
