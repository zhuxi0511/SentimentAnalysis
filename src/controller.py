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

def make_algorithm_init(algorithm_name):
    sys.path.append(const.config_dict['algorithm_dir'])
    import algorithm
    import preprocess 
    #TODO import the algorithm and preprocess AUTO
    import algorithm.maxent_baseline
    import algorithm.self_learn
    import algorithm.mln
    algorithm_dict = {
            'maxent_baseline': algorithm.maxent_baseline.MaxentBaseline,
            'self_learn': algorithm.self_learn.SelfLearn,
            'mln': algorithm.mln.Mln,
            }
    const.algorithm_handle = algorithm_dict.get(algorithm_name, None)()

    import preprocess.preprocess
    const.preprocess_handle = preprocess.preprocess.Preprocess(const.config_dict)

def preprocess_controller():
    logging.info('Preprocess controller start')

    preprocess_handle = const.preprocess_handle
    data_dir = const.config_dict['data_dir']

    file_list = os.popen('ls %s' % data_dir).readlines()
    for file_name in file_list:
        file_name = file_name.strip()
        if file_name.endswith('.raw'):
            f = open(os.path.join(data_dir, file_name))
            train.preprocess(preprocess_handle, f.readlines())
            util.save_extracted_content(preprocess_handle.extracted_content, file_name[:-4])
    util.save_feature_dict(preprocess_handle.feature_dict, 'feature_dict')

    logging.info('Preprocess controller end')


def combine_controller(run_date):
    logging.info('Combine controller start')

    # get config dictionary
    config_dict = const.config_dict
    algorithm_handle = const.algorithm_handle

    data_dir = config_dict['data_dir']
    train_file = config_dict['train_file']
    test_file = config_dict['test_file']

    train_file_list, status = util.list_file(data_dir, train_file)
    if status < 0:
        logging.error('train_file do not exist, check train_file in configure')
        return -1
    train.check_data(data_dir, train_file_list)

    test_file_list, status = util.list_file(data_dir, test_file, 'test')
    if status < 0:
        logging.error('test_file do not exist, check test_file in configure')
        return -1
    predict.check_data(data_dir, test_file_list)

    train_file = 'train'
    test_file = 'test'
    output_file = 'output'
    train.combine(algorithm_handle, train_file, test_file, output_file)
    predict.eval()

    predict.combine_save(config_dict['output_dir'],
            run_date, 
            (config_dict['algorithm'], config_dict['config_file'], 
                train_file_list, test_file_list))
    logging.info('Combin controller end')
    return 0

def train_controller(run_date):
    logging.info('Train controller start')
    # get config dictionary
    config_dict = const.config_dict
    algorithm_handle = const.algorithm_handle

    # train data to model
    data_dir = config_dict['data_dir']
    train_file = config_dict['train_file']

    train_file_list, status = util.list_file(data_dir, train_file)
    if status < 0:
        logging.error('train_file do not exist, check train_file in configure')
        return -1
    train.check_data(data_dir, train_file_list)
    train_file = 'train'
    model_file = 'model'

    train.train(algorithm_handle, train_file, model_file)

    model_dir = const.config_dict['model_dir']
    model.save(model_dir, run_date, 
            (config_dict['algorithm'], 
                train_file_list, 
                config_dict['config_file'], 
                config_dict['model_name']))

    logging.info('Train controller end')

def predict_controller(run_date):
    logging.info('Predict controller start')
    # get config dictionary
    config_dict = const.config_dict
    algorithm_handle = const.algorithm_handle

    data_dir = config_dict['data_dir']
    data_file = config_dict['test_file']

    test_file_list, status = util.list_file(data_dir, data_file, 'test')
    if status < 0:
        logging.error('test_file do not exist, check test_file in configure')
        return -1
    predict.check_data(data_dir, test_file_list)

    model_data = config_dict['test_model']
    model.load(data_dir, model_data)

    # predict the result
    test_file = 'test'
    model_file = 'model'
    output_file = 'output'
    predict.predict(algorithm_handle, test_file, model_file, output_file)
    predict.eval()

    predict.save(config_dict['output_dir'],
            run_date, 
            (config_dict['algorithm'], test_file_list))

    logging.info('Predict controller end')

def algorithm_controller(action, algorithm_name):
    # get the algorithm's information
    config_dict = const.config_dict
    algorithm_name = config_dict['check_algorithm']
    algorithm_handle = const.algorithm_dict[algorithm_name]
    if action == 'check':
        print algorithm_handle.information
