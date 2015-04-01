#!/user/bin/env python
# coding: utf-8

import os
import sys
import util

def update_model_info(local_model_info, name, date):
    """update_model_info(local_model_info, name, date)

    Create or update the model_info file.
    """
    fopt = open(local_model_info, 'w')
    fopt.write('This model is train by algorithm %s, the model\'s update date is %s\n' % (name, date))
    fopt.close()
    return 0

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
    """ % (algorithm, ' '.join(train_file_list))
    model_info_file = os.path.join(model_dir_with_time, 'info')
    os.system('echo %s > %s' % (model_content, model_info_file))

    os.system('cp %s %s' % (config_file, os.path.join(model_dir_with_time, 'config')))

