#!/user/bin/env python
# coding: utf-8

import os
import sys
import logging
import const

class MLN:

    def __init__(self):
        pass

    def data_adapter(data, adapted_data_file):
        f = open(adapted_data_file, 'w')
        for item_id, value in data.iteritems():
            line = '%s %s\n' % (value['tag'], 
                    ' '.join(map(lambda x:'%s:%s' % (x[0], x[1]), 
                        value['feature'].iteritems())))
            f.write(line)
        f.close()

    def train(self, data_file, model_file):
        pass

    def predict(self, test_file, model_file, output_file):
        pass

