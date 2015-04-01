#!/user/bin/env python
# coding: utf-8

import sys
import os
import util

def list_file(data_dir, data_file, class_of_data='train'):
    if data_file == 'ALL':
        name = '*'
    else:
        name = data_file
    data_file = os.path.join(data_dir, '%s.%s' % (name, class_of_data))
    res = os.popen('ls %s' % data_file)
    res_list = list(res.readlines())
    if len(res) == 0:
        return None, -1
    return map(lambda x:x.strip(), res_list), 0

def check_data(data_dir, data_file_list):
    os.system('rm -f train_data')
    for train_file in data_file_list:
        train_file = os.path.join(data_dir, '%s.train' % name)
        os.system('cat %s >> train_data')
    return 0

def preprocess(handle, lines):
    """Use preprocess handle to preprocess the raw lines"""

    return handle.preprocess(lines)

def data_adapter(handle, data, adapted_data_file):
    return handle.data_adapter(data, adapted_data_file)

def train(handle, train_file, model_file):
    """Use algorithm handle to train"""

    return handle.train(train_file, model_file)

def combine(handle, train_file, test_file, output_file):
    """Use algorithm handle to combine deal with train and test file"""

    return handle.combine(train_file, test_file, output_file)
