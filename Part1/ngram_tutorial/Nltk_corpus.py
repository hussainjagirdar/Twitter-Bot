import nltk
import string
import matplotlib.pyplot as plt
from nltk.util import ngrams
from operator import itemgetter
from collections import OrderedDict

corpus=nltk.corpus.brown
category_or_fileid='news'
stopwords=['','(',')','{','}','\\','--',':']
  
def corpus_details():
    sentences=corpus.sents(categories=category_or_fileid)
    text=[" ".join(sent_tokens) for sent_tokens in sentences]
    file_ids=corpus.fileids()
    categories=[]
    print(file_ids)
    try:
        categories=corpus.categories()
    except:
        categories=[]
    if categories:
        print(categories)
    readme=corpus.readme()
    print(readme)
    return text

corpus_text=corpus_details()
print type(corpus_text)

print corpus_text

      
def n_grams():
    unigram=[w.strip(string.punctuation).lower() for w in corpus.words()]
    unigram=[w for w in unigram if not w in stopwords]
    bigram =[a for a in ngrams(unigram,2)]
    trigram =[a for a in ngrams(unigram,3)]
    return unigram, bigram, trigram

unigram, bigram, trigram = n_grams()

def rank_graph(n_gram):
    frequency=nltk.FreqDist(n_gram)
    sorted_freq=OrderedDict(reversed(sorted(frequency.items(), key = itemgetter(1))))
    term_index={}
    freq_ngram=[]
    for i, key in enumerate(sorted_freq):
        term_index[i]=key
        freq_ngram.append(sorted_freq[key])
    plt.scatter(list(term_index.keys()), freq_ngram, color="orange", marker="*")
    plt.show()
    return term_index, freq_ngram 
    
term_index, freq_ngram=rank_graph(bigram)

#list(term_index.values())[:10]

