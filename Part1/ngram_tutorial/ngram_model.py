import nltk
import string
from nltk.util import ngrams
from math import log
stopwords=['']

corpus=nltk.corpus.brown
tokens=[w.strip(string.punctuation).lower() for w in corpus.words()]
tokens=[w for w in tokens if not w in stopwords]

spl =int(95*len(tokens)/100)
train_corpus = tokens[:spl]
test_corpus = tokens[spl:]

freq_1gram = nltk.FreqDist(train_corpus)
len_brown = len(train_corpus)
vocab=len(set(train_corpus))

def unigram_prob_with_add1smoothing(word):
    return (freq_1gram[ word] +1)/(len_brown + vocab)

cfreq_2gram = nltk.ConditionalFreqDist(nltk.bigrams(tokens, pad_left=True,pad_right=True,left_pad_symbol='<s>', right_pad_symbol="</s>"))
cprob_2gram = nltk.ConditionalProbDist(cfreq_2gram, nltk.MLEProbDist)
def bigram_prob_with_add1smoothing(word1, word2):
    cprob_2gram_add1=float((((1+cfreq_2gram[word1][word2])/(len(cfreq_2gram)+sum(cfreq_2gram[word1].values())))))
    return cprob_2gram_add1


trigrams_as_bigrams=[]
trigram =[a for a in ngrams(train_corpus,3,pad_left=True,pad_right=True,left_pad_symbol='<s>', right_pad_symbol="</s>")]
trigrams_as_bigrams.extend([((t[0],t[1]), t[2]) for t in trigram])
cfreq_3gram = nltk.ConditionalFreqDist(trigrams_as_bigrams)
cprob_3gram = nltk.ConditionalProbDist(cfreq_3gram, nltk.MLEProbDist)
def trigram_prob_with_add1smoothing(w1, w2, w3):
    cprob_3gram_add1=float((((1+cfreq_3gram[(w1,w2)][w3])/(len(cfreq_3gram)+sum(cfreq_3gram[(w1,w2)].values())))))
    return cprob_3gram_add1





def entropy(n, text):
        e = 0.0
        text = ["<s>"] + text + ["</s>"]
        for i in range(n - 1, len(text)):
            context = text[i - n + 1:i]
            token = text[i]
            #print(str(context)+"    "+token)
            e += logprob(token, context)
        return e / float(len(text) - (n - 1))


def logprob(word, context):
    if len(context)==0:
        p=unigram_prob_with_add1smoothing(word)
    elif len(context)==1:
        p=bigram_prob_with_add1smoothing(context[0], word)
    else:
        p=trigram_prob_with_add1smoothing(context[0], context[1], word)
    return -p*log(p , 2)

#logprob('at', ['smile'])

def perplexity(n, text):
      return pow(2.0, entropy(n, text))


entropy_value_2gram=entropy(2, test_corpus)

entropy_value_3gram=entropy(3, test_corpus)

perp_value_2gram=perplexity(2, test_corpus)

perp_value_3gram=perplexity(3, test_corpus)