# coding: utf-8

import sys
import os
from ICTCLAS2015 import nlpir

class WeiboPreprocess:
    def __init__(self):
        self.item_info = {}
        self.result_data = {}
        self.feature_dict = {}
        self.load_dictionary()

    def load_dictionary(self):
        file_dir = os.path.dirname(os.path.realpath(__file__))
        lexicon_dir = os.path.join(file_dir, 'lexicon')

        # weibo lexicon
        self.weibo_lexicon = {}
        f = open(os.path.join(lexicon_dir, 'InputLexicon.txt'))
        for line in f.readlines():
            line = line.strip().split()
            if not len(line) == 2:
                continue
            self.weibo_lexicon[line[0]] = {
                    'class':'weibo',
                    'polarity':int(line[1])
                    }
        f.close()

        #emotion lexicon
        self.emotion_lexicon = {}
        f = open(os.path.join(lexicon_dir, 'EmotionLexicon.txt'))
        for line in f.readlines():
            line = line.strip().split('\t')
            if not len(line) == 3:
                continue
            self.emotion_lexicon[line[0]] = {
                    'class':int(line[1]),
                    'polarity':int(line[2])
                    }
        f.close()

        #emotion lexicon
        self.negation_lexicon = {}
        f = open(os.path.join(lexicon_dir, 'NegationOperatorLexicon.txt'))
        for line in f.readlines():
            line = line.strip().split()
            if not len(line) == 1:
                continue
            self.negation_lexicon[line[0]] = {
                    'class':'negation',
                    'polarity':1
                    }
        f.close()

        #adverb_lexicon
        self.adverb_lexicon = {}
        f = open(os.path.join(lexicon_dir, 'StrengthenerAdverbLexicon.txt'))
        for line in f.readlines():
            line = line.strip().split()
            if not len(line) == 1:
                continue
            self.adverb_lexicon[line[0]] = {
                    'class':'adverb',
                    'polarity':1
                    }
        f.close()

        #ask_lexicon
        self.ask_lexicon= {}
        f = open(os.path.join(lexicon_dir, 'asked_word.txt'))
        for line in f.readlines():
            line = line.strip().split()
            if not len(line) == 1:
                continue
            self.ask_lexicon[line[0]] = {
                    'class':'ask',
                    'polarity':1
                    }
        f.close()

    def preprocess(self, lines):
        self.result_data = {}
        self.item_info = {}
        self.make_item_info(lines)
        segment_result = self.segment(self.item_info)
        self.extract_feature(segment_result)
        return self.result_data, self.feature_dict

    def segment(self, item_info):
        def add_word_class_polarity(word):
            w, pos, c, polarity = word[0], word[1], 'other', 1 
            for dictionary in [
                    self.adverb_lexicon, self.negation_lexicon,
                    self.emotion_lexicon, self.weibo_lexicon,
                    self.ask_lexicon]:
                if w in dictionary:
                    c = dictionary[w]['class']
                    polarity = dictionary[w]['polarity']
                    break
            return {'word':w, 'pos':pos, 'class':c, 'polarity':polarity}

        result = []
        for item_id, value in item_info.iteritems():
            content = []
            try:
                for word in nlpir.Seg(value['content']):
                    content.append(add_word_class_polarity(word))
            except Exception as e:
                print '!!!'
                print value
                print value['content']
                print e
                break
            value['content'] = content
            result.append((item_id, value))
        return result
    
    def extract_feature(self, segment_content):
        def add_feature(feature):
            if not feature:
                return 0
            if feature not in self.feature_dict:
                self.feature_dict[feature] = len(self.feature_dict) + 1
            return self.feature_dict[feature]
        
        #TODO need to confirm result_data format
        def add_result_data(item_id, feature_id, value=1):
            if not item_id in self.result_data:
                self.result_data[item_id] = {
                        'tag':self.item_info[item_id]['tag'],
                        'feature':{}
                        }
            feature_dict = self.result_data[item_id]['feature']
            if not feature_id in feature_dict:
                feature_dict[feature_id] = 0
            feature_dict[feature_id] += 1

        #词序列特征
        for item_id, value in segment_content:
            for i, word in enumerate(value['content']):
                #否定词 + 情感词 + 形容副词
                feature_id = None
                feature = None
                if word['class'] == 'negation':
                    for j, emotion_word in enumerate(value['content'][i+1:i+5]):
                        if emotion_word['pos'].startswith('w'):
                            break
                        if emotion_word['class'] == 'weibo' \
                                or isinstance(emotion_word['class'], int):
                            emotion_word_postion = j + i + 1
                            feature = '%s_%s' % (word['word'], emotion_word['word'])
                            for adverb_word in reversed(value['content'][i-2:emotion_word_postion]):
                                if adverb_word['class'] == 'adverb':
                                    feature = '%s_%s' % (feature, adverb_word['word'])
                                    break

                            break
                #情感词 + 形容副词
                elif word['class'] == 'weibo' or isinstance(word['class'], int):

                    has_negation_word = False
                    for negation_word in reversed(value['content'][i-4:i]):
                        if negation_word['pos'].startswith('w'):
                            break
                        if negation_word['class'] == 'negation':
                            has_negation_word = True
                            break
                    #如果有否定词表示已经被处理过，可跳过
                    if has_negation_word:
                        continue
                    for adverb_word in reversed(value['content'][i-2:i]):
                        if negation_word['pos'].startswith('w'):
                            break
                        if adverb_word['class'] == 'adverb':
                            feature = '%s_%s' % (word['word'], adverb_word['word'])
                            break
                if feature:
                    feature_id = add_feature(feature)
                    add_result_data(item_id, feature_id)

        # 处理item中各个情感词,情感词总极性以及其强度
        for item_id, value in segment_content:
            weibo_polarity = 0
            sentence_feature = None
            sentence_feature_id = None
            for i, word in enumerate(value['content']):
                if word['class'] == 'weibo' or isinstance(word['class'], int) \
                        or word['word'] in ['!', '?']:
                    feature = word['word']
                    feature_id = add_feature(feature)
                    add_result_data(item_id, feature_id)
                    if word['class'] == 'weibo':
                        weibo_polarity += word['polarity']
                    elif word['class'] == 1:
                        weibo_polarity += word['polarity']
                    elif isinstance(word['class'], int):
                        weibo_polarity -= word['polarity']
            if weibo_polarity > 0:
                sentence_feature = 'weibo_polarity_1'
            elif weibo_polarity == 0:
                sentence_feature = 'weibo_polarity_0'
            else:
                sentence_feature = 'weibo_polarity_-1'
            sentence_feature_id = add_feature(sentence_feature)
            add_result_data(item_id, sentence_feature_id)

            weibo_polarity = abs(weibo_polarity)
            polarity_strength = (weibo_polarity-1) / 3 + 1
            if polarity_strength >= 4:
                polarity_strength = 4
            sentence_feature = 'polarity_strength_%s' % polarity_strength
            sentence_feature_id = add_feature(sentence_feature)
            add_result_data(item_id, sentence_feature_id)
        
        #处理反问句以及句子长度特征
        for item_id, value in segment_content:
            ask_flag, negation_flag, sentiment_flag, question_flag = None, None, None, None
            feature, feature_id = None, None
            for i, word in enumerate(value['content']):
                if word['class'] == 'ask':
                    ask_flag = True
                elif word['class'] == 'negation':
                    if ask_flag:
                        negation_flag = True
                elif word['class'] == 'weibo' or isinstance(word['class'], int):
                    if ask_flag:
                        sentiment_flag = True
                elif word['word'] in ['!', '?']:
                    if sentiment_flag:
                        question_flag = True
            if question_flag and sentiment_flag and ask_flag:
                if not negation_flag:
                    feature = 'rhetorical'
                else:
                    feature = 'no_rhetorical'
            if feature:
                feature_id = add_feature(feature) 
                add_result_data(item_id, feature_id)

            item_length = len(value['content'])
            if item_length < 24:
                feature = 'length_1'
            elif item_length < 60:
                feature = 'length_2'
            elif item_length < 100:
                feature = 'length_3'
            else:
                feature = 'length_4'
            if feature:
                feature_id = add_feature(feature) 
                add_result_data(item_id, feature_id)


    def make_item_info(self, lines):
        for line in lines:
            line = line.strip().split('\t')
            if not line[0] in self.item_info:
                item = {'content':None, 'tag':None}
                self.item_info[line[0]] = item
            if len(line) >= 2:
                self.item_info[line[0]]['content'] = line[1]
            if len(line) >= 3:
                self.item_info[line[0]]['tag'] = line[2]

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
