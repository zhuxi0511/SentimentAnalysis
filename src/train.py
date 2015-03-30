#!/user/bin/env python
# coding: utf-8

import sys
import os
import util

def check_data(data_dir, train_data):
    if train_data == 'ALL':
        name = '*'
    else:
        name = train_data
    train_file = os.path.join(data_dir, '%s.train' % name)
    res = os.popen('ls %s' % train_file)
    if len(res.readlines()) == 0:
        return -1
    os.system('cat %s > train_data')
    return 0

def preprocess(handle, lines):
    """Use preprocess handle to preprocess the raw lines"""

    return handle.preprocess(lines)

def data_adapter(handle, data, adapted_data_file):
    return handle.data_adapter(data, adapted_data_file)

def train(handle, train_file, model_file):
    """Use algorthm handle to train"""

    return handle.train(train_file, model_file)

def combine(handle, train_file, test_file, output_file):
    """Use algorithm handle to combine deal with train and test file"""

    return handle.combine(train_file, test_file, output_file)
