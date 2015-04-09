#!/user/bin/env python
# coding: utf-8

import os
import sys
from maxent import MaxentModel

class SelfLearn:

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

    def combine(self, train_file, test_file, output_file):
        train_list = []
        f = open(train_file)
        for i, line in enumerate(f.readlines()):
            line = line.strip().split('\t')
            item_id = line[0]
            tag = line[1]
            context = map(lambda x:x.split(':'), line[2])
            context = tuple(map(lambda x:(x[0], float(x[1])), context))
            train_list.append( ('train%s' % item_id, context, tag) )

        # split train_list to 1:2 ==> oracle:train
        oracle_set = set(train_list[:len(train_list)/3])
        train_set = set(train_list[len(train_list)/3:])
        f.close()
        
        test_set = set()
        f = open(test_file)
        for i, line in enumerate(f.readlines()):
            item_id, tag, features = line.strip().split('\t')
            context = map(lambda x:x.split(':'), features)
            context = tuple(map(lambda x:(x[0], float(x[1])), context))
            test_set.add( ('test%s' % item_id, context, tag) )
        f.close()

        test_sum = len(test_set)
        oracle_sum = len(oracle_set)
        test_emotion_count = 0
        iter_upbound = 20
        iter_count = 0

        while test_emotion_count < 3560 and iter_count < iter_upbound:
            iter_count += 1
            self.maxent.begin_add_event()
            for sign, context, tag in train_set:
                context = list(context)
                if tag != '0':
                    if sign.startswith('train'):
                        self.maxent.add_event(context, tag, 4)
                    elif sign.startswith('oracle'):
                        self.maxent.add_event(context, tag, 6)
                    else:
                        self.maxent.add_event(context, tag, 3)
                else:
                    if sign.startswith('oracle'):
                        self.maxent.add_event(context, tag, 3)
                    else:
                        self.maxent.add_event(context, tag, 1)

            self.maxent.end_add_event()

            self.maxent.train(30, "lbfgs")

            test_eval_list = []
            for test_item in test_set:
                sign, context, tag = test_item
                context = list(context)
                max_tag = self.maxent.eval_all(context)[0]
                test_eval_list.append((max_tag, test_item))
            test_eval_list.sort(key=lambda x:x[0][1], reverse=True)
            for max_tag, test_item in test_eval_list[:test_sum/iter_upbound + 1]:
                sign, context, tag = test_item
                train_set.add( (sign, context, max_tag[0]) )
                test_set -= set([test_item])
                if max_tag[0] != '0':
                    test_emotion_count += 1
                    if test_emotion_count >= 3560:
                        break

            oracle_eval_list = []
            for oracle_item in oracle_set:
                sign, context, tag = oracle_item
                context = list(context)
                max_tag = self.maxent.eval_all(context)[0]
                oracle_eval_list.append((max_tag, oracle_item))
            oracle_eval_list.sort(key=lambda x:x[0][1])
            for max_tag, oracle_item in oracle_eval_list[:oracle_sum/iter_upbound + 1]:
                sign, context, tag = oracle_item
                train_set.add( ('oracle', context, tag) )
                oracle_set -= set([oracle_item])

            print 'iter count round %s' % iter_count
            print 'test emotion count = %s' % test_emotion_count

        answer_dict = {}
        for item in train_set:
            sign, context, tag = item
            if sign.startswith('test'):
                answer_dict[sign[4:]] = tag
        for item in test_set:
            sign, context, tag = item
            if sign.startswith('test'):
                answer_dict[sign[4:]] = '0'

        f = open(output_file, 'w')
        f.writelines(map(lambda x:'\t'.join(x)+'\n', 
            answer_dict.iteritems()))
        f.close()

    def train(self, data_file, model_file):
        ret = os.popen('maxent %s -m %s -i 30' % (data_file, model_file))

    def predict(self, test_file, model_file, output_file):
        ret = os.popen('maxent -p %s -m %s > %s' % (test_file, model_file, output_file))

if __name__ == '__main__':
    selflearn = SelfLearn()
    selflearn.combine('/home/zhuxi/weibo/data/weibo.train',
            '/home/zhuxi/weibo/data/weibo.test',
            '/home/zhuxi/weibo/data/self_learn_output')
