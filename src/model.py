#!/user/bin/env python
# coding: utf-8

import os
import sys
import util

def save(model_dir, run_date, model_info):
    """Save model to model_dir and add model info and date"""

    algorithm, algorithm_file, train_file_list, config_file, model_name = model_info
    if model_name == 'AUTO':
        model_name = '%s_%s' % run_date.get_date_hour()
    model_dir_with_name = os.path.join(model_dir, model_name)
    os.mkdir(model_dir_with_name)
    os.system('cp model %s' % model_dir_with_name)

    model_content = """Algorithm:%s
Train_file:%s
Model_name:%s
    """ % (algorithm, ' '.join(train_file_list), model_name)
    os.system('echo "%s" > %s' % (model_content, 'info'))
    model_info_file = os.path.join(model_dir_with_name, 'info')
    os.system('echo "%s" > %s' % (model_content, model_info_file))

    os.system('cp %s %s' % (config_file, os.path.join(model_dir_with_name, 'config')))
    os.system('cp %s %s' % (algorithm_file, model_dir_with_name))
    return 0

def load(model_dir, model_data):
    if model_data == 'AUTO':
        if not os.path.isfile('model'):
            return -2
    else:
        specify_model_file = os.path.join(model_dir, model_data, 'model')
        specify_model_info = os.path.join(model_dir, model_data, 'info')
        if not os.path.isfile(specify_model_file):
            return -1
        os.system('cp %s %s' % (specify_model_info, 'info'))
        return os.system('cp %s %s' % (specify_model_file, 'model'))
    return 0

