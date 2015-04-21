#coding:utf-8

def word_list(item_info, public_resource): 
    #词序列特征
    lexicon, segment_content = public_resource
    item_feature_list = []
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
                item_feature_list.append((item_id, feature))

    return item_feature_list

def emotion_word(item_info, public_resource):
    # 处理item中各个情感词,情感词总极性以及其强度

    lexicon, segment_content = public_resource
    item_feature_list = []

    for item_id, value in segment_content:
        weibo_polarity = 0
        sentence_feature = None
        for i, word in enumerate(value['content']):
            if word['class'] == 'weibo' or isinstance(word['class'], int) \
                    or word['word'] in ['!', '?']:
                feature = word['word']
                item_feature_list.append((item_id, feature))
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
        item_feature_list.append((item_id, sentence_feature))

        weibo_polarity = abs(weibo_polarity)
        polarity_strength = (weibo_polarity-1) / 3 + 1
        if polarity_strength >= 4:
            polarity_strength = 4
        sentence_feature = 'polarity_strength_%s' % polarity_strength
        item_feature_list.append((item_id, sentence_feature))
    return item_feature_list

def syntax(item_info, public_resource):
    #处理反问句特征

    lexicon, segment_content = public_resource
    item_feature_list = []

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
            item_feature_list.append((item_id, feature))
    return item_feature_list

def sentence_length(item_info, public_resource):
    #处理句子长度特征

    lexicon, segment_content = public_resource
    item_feature_list = []

    for item_id, value in segment_content:
        feature, feature_id = None, None
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
            item_feature_list.append((item_id, feature))
    return item_feature_list

