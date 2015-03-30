#!/user/bin/env python
# coding: utf-8

import os
import sys
import logging
import const

class Maxent:

    def __init__(self):
        pass

    def data_adapter(self, data, feature_dict, adapted_data_file):
        f = open(adapted_data_file, 'w')
        lines = []
        for item_id, value in data.iteritems():
            line = '%s %s\n' % (
                    value['tag'], 
                    ' '.join(
                        map(lambda x:'%s:%s' % (x[0], x[1]), 
                        value['feature'].iteritems())
                        )
                    )
            lines.append((item_id, line))
        lines.sort(key=lambda x:int(x[0]))
        f.writelines(map(lambda x:x[1], lines))
        f.close()

    def train(self, data_file, model_file):
        ret = os.popen('maxent %s -m %s -i 30' % (data_file, model_file))

    def predict(self, test_file, model_file, output_file):
        ret = os.popen('maxent -p %s -m %s > %s' % (test_file, model_file, output_file))

