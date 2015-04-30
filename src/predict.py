#!/user/bin/env python
# coding: utf-8

import os
import sys
import util

def check_data(data_dir, data_file_list):
    os.system('rm -f test')
    for file_name in data_file_list:
        test_file = os.path.join(data_dir, '%s' % file_name)
        os.system('cat %s >> test' % test_file)
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

def save(output_dir, run_date, predict_info):
    """Save predict output to output_dir and add test file info and model info"""

    algorithm, test_file_list = predict_info
    algorithm_file = '%s.py' % algorithm
    time = '%s_%s' % run_date.get_date_hour()
    output_dir_with_time = os.path.join(output_dir, time)
    os.mkdir(output_dir_with_time)
    os.system('cp info %s' % os.path.join(output_dir_with_time, 'info'))
    os.system('cp eval %s' % os.path.join(output_dir_with_time, 'eval'))
    os.system('cp output %s' % os.path.join(output_dir_with_time, 'output'))
    os.system('cp %s %s' % (algorithm_file, output_dir_with_time))
    predict_content = """Test_file:%s
Test_time:%s
    """ % (' '.join(test_file_list), time)
    predict_info_file = os.path.join(output_dir_with_time, 'info')
    os.system('echo "%s" >> %s' % (predict_content, predict_info_file))
    return 0

def combine_save(output_dir, run_date, combine_info):
    """Save combine output to output_dir and add test file info and model info"""

    algorithm, config_file, train_file_list, test_file_list = combine_info
    algorithm_file = '%s.py' % algorithm
    time = '%s_%s' % run_date.get_date_hour()
    output_dir_with_time = os.path.join(output_dir, time)
    os.mkdir(output_dir_with_time)
    os.system('cp eval %s' % os.path.join(output_dir_with_time, 'eval'))
    os.system('cp output %s' % os.path.join(output_dir_with_time, 'output'))
    os.system('cp %s %s' % (config_file, os.path.join(output_dir_with_time, 'config')))
    os.system('cp %s %s' % (algorithm_file, output_dir_with_time))
    predict_content = """Algorithm:%s
Train_file:%s
Test_file:%s
Run_time:%s
    """ % (algorithm, ' '.join(train_file_list), ' '.join(test_file_list), time)
    predict_info_file = os.path.join(output_dir_with_time, 'info')
    os.system('echo "%s" >> %s' % (predict_content, predict_info_file))
    return 0
