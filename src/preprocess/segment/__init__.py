from ICTCLAS2015 import nlpir

def ictclas2015(item_info):
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
 
