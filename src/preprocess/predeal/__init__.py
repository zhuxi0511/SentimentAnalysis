import os
from ICTCLAS2015 import nlpir

def maxent_predeal(item_info):
    def load_dictionary():
        file_dir = os.path.dirname(os.path.realpath(__file__))
        lexicon_dir = os.path.join(file_dir, 'lexicon')
        lexicon = {}

        # weibo lexicon
        lexicon['weibo_lexicon'] = {}
        f = open(os.path.join(lexicon_dir, 'InputLexicon.txt'))
        for line in f.readlines():
            line = line.strip().split()
            if not len(line) == 2:
                continue
            lexicon['weibo_lexicon'][line[0]] = {
                    'class':'weibo',
                    'polarity':int(line[1])
                    }
        f.close()

        #emotion lexicon
        lexicon['emotion_lexicon'] = {}
        f = open(os.path.join(lexicon_dir, 'EmotionLexicon.txt'))
        for line in f.readlines():
            line = line.strip().split('\t')
            if not len(line) == 3:
                continue
            lexicon['emotion_lexicon'][line[0]] = {
                    'class':int(line[1]),
                    'polarity':int(line[2])
                    }
        f.close()

        #emotion lexicon
        lexicon['negation_lexicon'] = {}
        f = open(os.path.join(lexicon_dir, 'NegationOperatorLexicon.txt'))
        for line in f.readlines():
            line = line.strip().split()
            if not len(line) == 1:
                continue
            lexicon['negation_lexicon'][line[0]] = {
                    'class':'negation',
                    'polarity':1
                    }
        f.close()

        #adverb_lexicon
        lexicon['adverb_lexicon'] = {}
        f = open(os.path.join(lexicon_dir, 'StrengthenerAdverbLexicon.txt'))
        for line in f.readlines():
            line = line.strip().split()
            if not len(line) == 1:
                continue
            lexicon['adverb_lexicon'][line[0]] = {
                    'class':'adverb',
                    'polarity':1
                    }
        f.close()

        #ask_lexicon
        lexicon['ask_lexicon']= {}
        f = open(os.path.join(lexicon_dir, 'asked_word.txt'))
        for line in f.readlines():
            line = line.strip().split()
            if not len(line) == 1:
                continue
            lexicon['ask_lexicon'][line[0]] = {
                    'class':'ask',
                    'polarity':1
                    }
        f.close()
        return lexicon

    def add_word_class_polarity(word, lexicon):
        w, pos, c, polarity = word[0], word[1], 'other', 1 
        for dictionary in [
                lexicon['adverb_lexicon'], lexicon['negation_lexicon'],
                lexicon['emotion_lexicon'], lexicon['weibo_lexicon'],
                lexicon['ask_lexicon']]:
            if w in dictionary:
                c = dictionary[w]['class']
                polarity = dictionary[w]['polarity']
                break
        return {'word':w, 'pos':pos, 'class':c, 'polarity':polarity}

    def ictclas2015(item_info, lexicon):
        result = []
        for item_id, value in item_info.iteritems():
            content = []
            try:
                for word in nlpir.Seg(value['content']):
                    content.append(add_word_class_polarity(word, lexicon))
            except Exception as e:
                print '!!!'
                print value
                print value['content']
                print e
                break
            value['content'] = content
            result.append((item_id, value))
        return result

    lexicon = load_dictionary()
    segment_content = ictclas2015(item_info, lexicon)
    return (lexicon, segment_content)
 
