#!/user/bin/env python
# coding: utf-8

import os
import sys
import logging
import util

def get_data_to_local(hadoop_bin, source_dir, target_file):
    """get_data_to_local(hadoop_bin, source_dir, target_file)

    Use hadoop_bin to get files from hdfs's source_dir to local's target_file,
    the files in source_dir will be merged into one file.
    """

    ret = util.get_file_to_local(hadoop_bin, source_dir, target_file, 'dir')
    if not 0 == ret:
        logging.warning('Model get_data function in model failed')
        return 1
    return 0

def save_model(hadoop_bin, source_model_dir, target_dir, date):
    """save_model(hadoop_bin, source_model_dir, target_dir, date)

    Use hadoop_bin to put model from source_model_dir to hadoop_bin by date,
    the model file and model_info file will be put.
    """
    os.system('rm %s/.model.crc' % source_model_dir)
    ret = util.put_file_to_hadoop(hadoop_bin, os.path.join(target_dir, date, 'model'), 
            os.path.join(source_model_dir, 'model'))
    ret |= util.put_file_to_hadoop(hadoop_bin, os.path.join(target_dir, 'model_info'), 
            os.path.join(source_model_dir, 'model_info'))
    if not 0 == ret:
        logging.warning("Model save_model function in model failed")
        return 1
    return 0

def update_model_info(local_model_info, name, date):
    """update_model_info(local_model_info, name, date)

    Create or update the model_info file.
    """
    fopt = open(local_model_info, 'w')
    fopt.write('This model is train by algorithm %s, the model\'s update date is %s\n' % (name, date))
    fopt.close()
    return 0

def save_to_hadoop(hadoop_bin, local_model_dir, hadoop_model_dir, algorithm_handle, date):
    local_model_info = os.path.join(local_model_dir, 'model_info')
    ret = update_model_info(local_model_info, algorithm_handle.name, date)
    ret |= save_model(hadoop_bin, local_model_dir, hadoop_model_dir, date)
    return ret
