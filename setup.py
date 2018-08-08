#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017+ Gradiant, Vigo, Spain

from setuptools import setup, find_packages
from version import *

setup(
    name='bob.gradiant.pad.evaluator',
    version=get_version(),
    description='This package implements the face-PAD evaluation framework proposed by Gradiant (AUE, ACE, E2E)',
    url='http://pypi.python.org/pypi/template-gradiant-python',
    license='BSD-3',
    author='Biometrics Team (Gradiant)',
    author_email='biometrics.support@gradiant.org',
    long_description=open('README.md').read(),
    keywords='evaluation face pad gradiant aue ace e2e',

    # This line is required for any distutils based packaging.
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,

    install_requires=[
      "setuptools",
    ],

    entry_points={
      'console_scripts': [
        'create_configuration_file.py = bob.gradiant.pad.evaluator.scripts.create_configuration_file:main',
        'algorithmic_unconstrained_evaluation.py = bob.gradiant.pad.evaluator.scripts.algorithmic_unconstrained_evaluation:main',
        'algorithmic_constrained_evaluation.py = bob.gradiant.pad.evaluator.scripts.algorithmic_constrained_evaluation:main',
        'end_to_end_evaluation.py = bob.gradiant.pad.evaluator.scripts.end_to_end_evaluation:main',
      ],
    },
)
