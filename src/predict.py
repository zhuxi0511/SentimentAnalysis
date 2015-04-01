#!/user/bin/env python
# coding: utf-8

import sys
import util

def check_data(data_dir, data_file_list):
    os.system('rm -f test_data')
    for train_file in data_file_list:
        train_file = os.path.join(data_dir, '%s.test' % name)
        os.system('cat %s >> test_data')
    return 0

def predict(handle, test_file, model_file, output_file):
    """Use algorithm handle to predict"""

    return handle.predict(test_file, model_file, output_file)

