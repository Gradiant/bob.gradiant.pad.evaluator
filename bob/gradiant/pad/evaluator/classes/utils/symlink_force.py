#!/usr/bin/env python
# Gradiant's Biometrics Team <biometrics.support@gradiant.org>
# Copyright (C) 2017 Gradiant, Vigo, Spain
import os
import errno


def symlink_force(target, link_name):
    target = os.path.abspath(target)
    try:
        os.symlink(target, link_name)
    except OSError, e:
        if e.errno == errno.EEXIST:
            try:
                os.remove(link_name)
                os.symlink(target, link_name)
            except:
                raise RuntimeError(
                    'You are trying to use an external data \'{}\', when you already have extracted on your folder \'{}\''.format(
                        target, link_name))
        else:
            raise e