#!/user/bin/env python
# coding: utf-8

import sys
import util

def predict(handle, local_model, local_output):
    return handle.predict(local_model, local_output)

def save_output_to_hadoop(hadoop_bin, output_file, local_output_file):
    return util.put_file_to_hadoop(hadoop_bin, output_file, local_output_file)
