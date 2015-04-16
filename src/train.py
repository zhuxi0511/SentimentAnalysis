#!/user/bin/env python
# coding: utf-8

import sys
import os
import util

def check_data(data_dir, data_file_list):
    """Check and combine all train data to tmp dir for training"""

    os.system('rm -f train')
    for file_name in data_file_list:
        train_file = os.path.join(data_dir, '%s' % file_name)
        os.system('cat %s >> train' % train_file)
    return 0

def preprocess(handle, lines):
    """Use preprocess handle to preprocess the raw lines"""

    return handle.preprocess(lines)

def train(handle, train_file, model_file):
    """Use algorithm handle to train"""

    return handle.train(train_file, model_file)

def combine(handle, train_file, test_file, output_file):
    """Use algorithm handle to combine deal with train and test file"""

    return handle.combine(train_file, test_file, output_file)
