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
        self.public_resource = self.pretreat(self.item_info)
        self.extract(self.public_resource)

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

    def pretreat(self, item_info):
        pretreat_module = self.config_dict['pretreat_module']
        exec('from pretreat import %s' % pretreat_module)
        pretreat_function = eval(pretreat_module)
        return pretreat_function(item_info)

    def extract(self, public_resource):
        self.extracted_content = {}
        extract_module_list = self.config_dict['extract_module']
        for extract_module in extract_module_list:
            exec('from extract import %s' % extract_module)
            extract_funcion = eval(extract_module)
            item_feature_list = extract_funcion(self.item_info, public_resource)
            for item, feature in item_feature_list:
                feature_id = self.add_feature(feature)
                self.add_extracted_content(item, feature_id)

    def add_feature(self, feature):
        if not feature:
            return 0
        if feature not in self.feature_dict:
            self.feature_dict[feature] = len(self.feature_dict) + 1
        return self.feature_dict[feature]

    def add_extracted_content(self, item_id, feature_id, value=1):
        if not item_id in self.extracted_content:
            self.extracted_content[item_id] = {
                    'tag':self.item_info[item_id]['tag'],
                    'feature':{}
                    }
        feature_dict = self.extracted_content[item_id]['feature']
        if not feature_id in feature_dict:
            feature_dict[feature_id] = 0
        feature_dict[feature_id] += value

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
