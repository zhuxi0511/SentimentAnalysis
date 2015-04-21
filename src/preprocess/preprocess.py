# coding: utf-8

import sys
import os

class Preprocess:
    def __init__(self, config_dict):
        self.config_dict = config_dict
        self.item_info = {}
        self.extracted_content = {}
        self.feature_dict = {}

    def preprocess(self, lines):
        self.item_info = self.read_raw(lines)
        self.public_resource = self.predeal(self.item_info)
        self.extracted_content = self.extract(self.public_resource)

    def read_raw(self, lines):
        item_info = {}
        for line in lines:
            line = line.strip().split('\t')
            if not line[0] in self.item_info:
                item = {'content':None, 'tag':None}
                item_info[line[0]] = item
            if len(line) >= 2:
                item_info[line[0]]['content'] = line[1]
            if len(line) >= 3:
                item_info[line[0]]['tag'] = line[2]
        return item_info

    def predeal(self, item_info):
        pass

    def extract(self, segmented_content):
        pass

def output(result, feature_dict):
    t_dict = {}
    for feature, feature_id in feature_dict.iteritems():
        t_dict[feature_id] = feature

    for item_id, value in result.iteritems():
        print '%s\t%s\t%s' % (value['tag'], item_id, ' '.join(map(lambda x:'%s:%s' % (x[0], x[1]), value['feature'].iteritems())))


if __name__ == '__main__':
    pre = WeiboPreprocess()
    f = open('/home/zhuxi/weibo/data/weibo.train.raw')
    pre.preprocess(f.readlines())
    output(pre.result_data, pre.feature_dict)
