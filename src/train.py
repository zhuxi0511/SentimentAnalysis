#!/user/bin/env python
# coding: utf-8

import sys
import util

def preprocess(handle, lines):
    """Use preprocess handle to preprocess the raw lines"""

    return handle.preprocess(lines)

def data_adapter(handle, data, adapted_data_file):
    return handle.data_adapter(data, adapted_data_file)

def train(handle, data_file, model_file):
    """Use algorthm handle to train"""

    return handle.train(data_file, model_file)

def combine(handle, train_file, test_file, output_file):
    """Use algorithm handle to combine deal with train and test file"""

    return handle.combine(train_file, test_file, output_file)
