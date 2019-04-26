from mainapp.models import Frame
from mainapp.functions import temp
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.stem.porter import *
import numpy as np
np.random.seed(2018)
import enchant

import nltk
nltk.download('wordnet')


def lemmatize_stemming(text):
    return WordNetLemmatizer().lemmatize(text, pos='v')


def preprocess(text):
    result = []
    d = enchant.Dict("en_US")
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            t = lemmatize_stemming(token)
            if d.check(t):
                result.append(t)
    return result


def topic_model():
    frames = Frame.objects.filter(f_type="SLIDE").order_by('id').all()
    docs = []
    for each in frames:
        # print(each.content)
        # print("------")
        docs.append(each.content)

    pre_processed = []
    for each in docs:
        pre_processed.append(preprocess(text=each))
    t = temp.start_topic_modelling(test=pre_processed)
    print(t)

    final = []

    slide = 1
    for each in frames:
        try:
            navigation = {}
            navigation["timestamp"] = int(each.timestamp)
            navigation["topic"] = t["slide" + str(slide)]
            slide += 1
            final.append(navigation)
        except Exception:
            pass
    return final
