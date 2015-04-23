#!/user/bin/env python
# coding: utf-8

import os
import sys
import logging
import const
from maxent import MaxentModel

class MaxentBaseline:

    def __init__(self):
        self.maxent = MaxentModel()

    def train(self, train_file, model_file):
        f = open(train_file)
        self.maxent.begin_add_event()
        for line in f.readlines():
            item_id, tag, features = line.strip().split('\t')
            features = map(lambda x:x.split(':'), features.split(' '))
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
            features = map(lambda x:x.split(':'), features.split(' '))
            features = map(lambda x:(x[0], float(x[1])), features)
            max_tag = self.maxent.eval_all(features)[0][0]
            of.write('%s\t%s\n' % (item_id, max_tag))
        of.close()
        f.close()
