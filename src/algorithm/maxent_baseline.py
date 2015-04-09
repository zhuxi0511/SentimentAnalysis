#!/user/bin/env python
# coding: utf-8

import os
import sys
import logging
import const
from maxent import MaxentModel

class Maxent:

    def __init__(self):
        self.maxent = MaxentModel()

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

    def train(self, train_file, model_file):
        f = open(train_file)
        self.maxent.begin_add_event()
        for line in f.readlines():
            item_id, tag, features = line.strip().split('\t')
            features = map(lambda x:x.split(':'), features)
            features = map(lambda x:(x[0], float(x[1])), features)
            if tag != '0':
                self.maxent.add_event(features, tag, 4)
            else:
                self.maxent.add_event(features, tag, 1)
        self.maxent.end_add_event()

        self.maxent.train(30, 'lbfgs')
        self.maxent.save(model_file)

    def predict(self, test_file, model_file, output_file):
        self.maxent.load(model_file)
        f = open(test_file)
        of = open(output_file, 'w')
        for line in f.readlines():
            item_id, tag, features = line.strip().split('\t')
            features = map(lambda x:x.split(':'), features)
            features = map(lambda x:(x[0], float(x[1])), features)
            max_tag = self.maxent.evalall(features)[0][0]
            of.write('%s\t%s\n' % (item_id, max_tag))
        of.close()
        f.close()
