#!/user/bin/env python
# coding: utf-8

import os
import sys
import logging
import const
import train
import model
import predict
import util
algorithm_dir = const.config_dict['algorithm_dir']
sys.path.append(algorithm_dir)
import algorithm
from preprocess import weibo_preprocess

#TODO init the algorithm after read the config file
def make_algorithm_init(algorithm_name):
    import algorithm.maxent
    algorithm_dict = {
            'maxent': algorithm.maxent.Maxent
            }
    const.algorithm_handle = algorithm_dict.get(algorithm_name, None)()
    const.preprocess_handle = weibo_preprocess.WeiboPreprocess()

def combine_controller():
    logging.info('Combine controller start')

    # get config dictionary
    config_dict = const.config_dict
    algorithm_handle = const.algorithm_handle

    data_dir = const.config_dict['data_dir']
    if train.check_data(data_dir, config_dict['train_data']) < 0:
        logging.error('train_data donot exist, check train_data in configure')
        return -1

    train_file = 'train_data'
    test_file = 'test_data'
    train.combine(algorithm_handle, train_file, test_file, output_file)

    logging.info('Combin controller end')
    return 0

def preprocess_controller():
    logging.info('Preprocess controller start')
    preprocess_handle = const.preprocess_handle
    algorithm_handle = const.algorithm_handle
    data_dir = const.config_dict['data_dir']
    print const.config_dict['data_dir']
    print const.config_dict['log_dir']
    file_list = os.popen('ls %s' % data_dir).readlines()
    for file_name in file_list:
        file_name = file_name.strip()
        if file_name.endswith('.raw'):
            preprocess_lines = open(os.path.join(data_dir, file_name)).readlines()
            result_data, feature_dict = train.preprocess(preprocess_handle, preprocess_lines)
            algorithm_handle.data_adapter(result_data, feature_dict, os.path.join(data_dir, file_name[:-4]))
    logging.info('Preprocess controller end')

def train_controller():
    logging.info('Train controller start')
    # get config dictionary
    config_dict = const.config_dict
    algorithm_handle = const.algorithm_handle

    # train data to model
    #train.check_data(algorithm_handle)
    data_dir = const.config_dict['data_dir']
    model_dir = const.config_dict['model_dir']
    #TODO specify file
    data_file = os.path.join(data_dir, 'weibo.train')
    model_file = os.path.join(model_dir, 'model')
    train.train(algorithm_handle, data_file, model_file)

    logging.info('Train controller end')

def predict_controller():
    logging.info('Predict controller start')
    # get config dictionary
    config_dict = const.config_dict
    algorithm_handle = const.algorithm_handle

    # predict the result
    local_output_file = os.path.join(config_dict['project_dir'], 'data', 'output')
    predict.predict(algorithm_handle, local_model_file, local_output_file)
    output_file = os.path.join(config_dict['output_dir'], date, 'output')
    logging.info('Predict controller end')

def algorithm_controller(action, algorithm_name):
    # get the algorithm's information
    config_dict = const.config_dict
    algorithm_name = config_dict['check_algorithm']
    algorithm_handle = const.algorithm_dict[algorithm_name]
    if action == 'check':
        print algorithm_handle.information
