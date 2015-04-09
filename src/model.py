#!/user/bin/env python
# coding: utf-8

import os
import sys
import util

def save(model_dir, run_date, model_info):
    """Save model to model_dir and add model info and date"""

    time = '%s_%s' % run_date.get_date_hour
    model_dir_with_time = os.path.join(model_dir, time)
    os.mkdir(model_dir_with_time)
    os.system('cp model %s' % model_dir_with_time)

    algorithm, train_file_list, config_file = model_info
    model_content = """
        Algorithm:%s
        Train_file:%s
        Train_time:%s
    """ % (algorithm, ' '.join(train_file_list), time)
    os.system('echo %s > %s' % (model_content, 'info'))
    model_info_file = os.path.join(model_dir_with_time, 'info')
    os.system('echo %s > %s' % (model_content, model_info_file))

    os.system('cp %s %s' % (config_file, os.path.join(model_dir_with_time, 'config')))
    return 0

def load(model_dir, model_data):
    if model_data == 'AUTO':
        if not os.path.isfile('model'):
            return -2
    else:
        specify_model_file = os.path.join(model_dir, model_data, 'model')
        if not os.path.isfile(specify_model_file):
            return -1
        return os.system('cp %s %s' % (specify_model_file, 'model'))
    return 0

