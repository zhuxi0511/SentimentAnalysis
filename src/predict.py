#!/user/bin/env python
# coding: utf-8

import sys
import util

def check_data(data_dir, data_file_list):
    os.system('rm -f test')
    for train_file in data_file_list:
        train_file = os.path.join(data_dir, '%s.test' % name)
        os.system('cat %s >> test')
    return 0

def predict(handle, test_file, model_file, output_file):
    """Use algorithm handle to predict"""

    return handle.predict(test_file, model_file, output_file)

def eval():
    right_sum, p_sum, r_sum = 0.0, 0, 0
    standard = {}
    f = open('test')
    for line in f.readlines():
        item_id, tag, features = line.strip().split('\t')
        standard[item_id] = tag
        if tag != '0':
            r_sum += 1
    f.close()

    f = open('output')
    for line in f.readlines():
        item_id, tag = line.strip().split('\t')
        if tag != '0':
            p_sum += 1
        if tag == standard.get(item_id, None):
            right_sum += 1
    f.close()
    P = right_sum / p_sum
    R = right_sum / r_sum
    F = 2 * P * R / (P + R)
    f = open('eval', 'w')
    f.write('P: %s\n' % P)
    f.write('R: %s\n' % R)
    f.write('F: %s\n' % F)
    f.close()

