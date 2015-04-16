#!/user/bin/env python
# coding: utf-8

import sys
import os
import ConfigParser
import logging
import datetime
from optparse import OptionParser

def get_value(config, section, key, error=None):
    try:
        value = config.get(section, key)
    except:
        if error:
            print >> sys.stderr, "try to get %s in %s failed, %s" % (key, section, error)
            sys.exit(-1)
        else:
            return None
    return value

def get_dir(config, section, key, error=None):
    try:
        value = config.get(section, key)
    except:
        if error:
            print >> sys.stderr, "try to get %s in %s failed, %s" % (key, section, error)
            sys.exit(-1)
        else:
            return None
    return os.path.realpath(os.path.expanduser(value))

if __name__ == '__main__':
    #get config file path
    src_dir = os.path.dirname(os.path.realpath(__file__))
    start_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    # add src path
    sys.path.append(src_dir)
    import const
    import controller
    tmp_dir = os.path.join(src_dir, 'tmp')
    os.system('mkdir -p %s' % tmp_dir)
    os.chdir(tmp_dir)

    #get command option
    parser = OptionParser()
    parser.add_option('--preprocess', dest='preprocess', action='store_true',
            help='To confire whether need preprocess')
    parser.add_option('--train', dest='train', action='store_true',
            help='To confirm whether train model')
    parser.add_option('--predict', dest='predict', action='store_true', 
            help='To confirm whether predict model')
    parser.add_option('--combine', dest='combine', action='store_true', 
            help='To confirm whether combine model(traditional method connot do)')
    parser.add_option('--check_model', dest='check_model', action='store_true', 
            help='Check model\'s information')
    parser.add_option('--delete_model', dest='delete_model', action='store_true', 
            help='Delete model file')
    parser.add_option('--check_algo', dest='check_algorithm', action='store', metavar='ALGORITHMNAME', 
            help='Check the appoint algorithm\'s information')

    (option, args) = parser.parse_args()
    print option, args
    if len(args) != 1:
        print >> sys.stderr, "Param Error. Using: %s %s" % (sys.argv[0], 'config')
        sys.exit(1)
    config_file = args[0]

    #get config file option
    config = ConfigParser.ConfigParser()
    try:
        config.read(config_file)
    except:
        print >> sys.stderr, 'error with reading config file'
        sys.exit(-1)
    config_dict = const.config_dict
    config_dict['config_file'] = config_file
    config_dict['algorithm_dir'] = get_value(config, 'INIT', 'algorithm_dir', 
            '[INIT] does not have algorithm_dir option')
    config_dict['algorithm'] = get_value(config, 'INIT', 'algorithm', 
            '[INIT] does not have algorithm option')
    config_dict['data_dir'] = get_dir(config, 'DATA', 'data_dir', 
            '[DATA] does not have data_dir option')
    config_dict['model_dir'] = get_dir(config, 'DATA', 'model_dir', 
            '[DATA] does not have model_dir option')
    config_dict['log_dir'] = get_dir(config, 'DATA', 'log_dir', 
            '[DATA] does not have log_dir option')
    config_dict['output_dir'] = get_dir(config, 'DATA', 'output_dir', 
            '[DATA] does not have output_dir option')
    config_dict['feature_extract'] = get_value(config, 'TRAIN', 'feature_extract', 
            '[TRAIN] does not have feature_extract option')
    config_dict['feature_extract'] = config_dict['feature_extract'].split(' ')
    config_dict['train_file'] = get_value(config, 'TRAIN', 'train_file', 
            '[TRAIN] does not have train_file option')
    config_dict['model_name'] = get_value(config, 'TRAIN', 'model_name', 
            '[TRAIN] does not have model_name option')
    config_dict['test_file'] = get_value(config, 'PREDICT', 'test_file', 
            '[PREDICT] does not have predict_data option')
    config_dict['test_model'] = get_value(config, 'PREDICT', 'test_model', 
            '[PREDICT] does not have test_model option')

    #Make director for log model and output
    #Then initialize log file
    log_dir = config_dict['log_dir']
    os.system('mkdir -p %s' % log_dir)
    os.system('mkdir -p %s' % config_dict['model_dir'])
    os.system('mkdir -p %s' % config_dict['output_dir'])
    logging.basicConfig(filename=os.path.join(log_dir,start_time), level=logging.DEBUG,
            filemode = 'a', format = '%(asctime)s - %(levelname)s: %(message)s')
    logging.info('analysis platform start in time %s' % start_time)

    controller.make_algorithm_init(config_dict['algorithm'])

    #check the option and do the action
    if option.check_model:
        controller.model_controller('check')

    if option.check_algorithm:
        controller.algorithm_controller('check', option.check_algorithm)

    from util import DateHour
    run_date = DateHour()
    if option.combine:
        controller.combine_controller()
    else:
        if option.preprocess:
            controller.preprocess_controller()

        if option.train:
            controller.train_controller(run_date)

        if option.predict:
            controller.predict_controller(run_date)

    logging.info('analysis platform finished successful')
    sys.exit(0)
