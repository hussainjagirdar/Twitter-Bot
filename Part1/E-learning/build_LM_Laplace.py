import string
import nltk
from nltk.util import ngrams
import math
from nltk.tokenize import word_tokenize
stopwords=['','(',')','{','}','\\','--',':']

database=open("lakh.txt",'r')

line =database.readline()
index=0
tokenList=[]
while line:
    tokens=[w.strip(string.punctuation).lower() for w in word_tokenize(line)]
    tokens=[w for w in tokens if not w in stopwords]
    tokenList.append('<s>')
    tokenList.extend(tokens)
    tokenList.append('</s>')
    line=database.readline()
    index+=1
    if index%10000==0:
        print index

tokens=tokenList
#print "tokenlist=",tokens

spl =int(95*len(tokens)/100)
train_corpus = tokens[:spl]
test_corpus = tokens[spl:]

def n_grams():
    unigram=[w.lower() for w in train_corpus]
    bigram =[a for a in ngrams(unigram,2)]
    trigram =[a for a in ngrams(unigram,3)]
    return unigram, bigram, trigram

unigram, bigram, trigram = n_grams()
#print unigram
#print bigram
#print unigram
freq_1gram = nltk.FreqDist(train_corpus)
len_brown = len(train_corpus)
vocab=len(set(train_corpus))

def unigram_prob(word):
    return freq_1gram[ word] / len_brown
cfreq_2gram = nltk.ConditionalFreqDist(nltk.bigrams(tokens))
cprob_2gram = nltk.ConditionalProbDist(cfreq_2gram, nltk.LaplaceProbDist)
 
def bigram_prob(word1, word2):
    return cprob_2gram[word1].prob(word2)
#
#cprob_2gram["betting"].prob("men")
#bigram_prob("betting","men")

trigrams_as_bigrams=[]
trigram =[a for a in ngrams(train_corpus,3,pad_left=True,pad_right=True,left_pad_symbol='<s>', right_pad_symbol="</s>")]
trigrams_as_bigrams.extend([((t[0],t[1]), t[2]) for t in trigram])
cfreq_3gram = nltk.ConditionalFreqDist(trigrams_as_bigrams)
cprob_3gram = nltk.ConditionalProbDist(cfreq_3gram, nltk.LaplaceProbDist)
def trigram_prob(w1, w2, w3):
    if not cprob_3gram.has_key((w1,w2)):
        return float(1)/len(cprob_3gram)
    return cprob_3gram[(w1, w2)].prob(w3)

def unigram_prob_with_add1smoothing(word):
    return float(freq_1gram[ word] +1)/(len_brown + vocab)
def bigram_prob_with_add1smoothing(word1, word2):
    cprob_2gram_add1=float((((float(1+cfreq_2gram[word1][word2]))/(len(cfreq_2gram)+sum(cfreq_2gram[word1].values())))))
    return cprob_2gram_add1
def trigram_prob_with_add1smoothing(w1, w2, w3):
    cprob_3gram_add1=float((((float(1+cfreq_3gram[(w1,w2)][w3]))/(len(cfreq_3gram)+sum(cfreq_3gram[(w1,w2)].values())))))
    return cprob_3gram_add1

def entropy(n, text):
        e = 0.0
        text = ["<s>"] + text + ["</s>"]
        for i in range(n - 1, len(text)):
            context = text[i - n + 1:i]
            token = text[i]
            e += logprob(token, context)
        return e / float(len(text) - (n - 1))


def logprob(word, context):
    if len(context)==0:
        p=unigram_prob_with_add1smoothing(word)
    elif len(context)==1:
        p=bigram_prob(context[0], word)
    else:
        p=trigram_prob(context[0], context[1], word)
    return -p*math.log(p , 2)

#logprob('at', ['smile'])

def perplexity(n, text):
      return pow(2.0, entropy(n, text))

entropy_value_2gram=entropy(2, test_corpus)
print entropy_value_2gram

perp_value_2gram=perplexity(2, test_corpus)
print perp_value_2gram

entropy_value_3gram=entropy(3, test_corpus)
print entropy_value_3gram

perp_value_3gram=perplexity(3, test_corpus)
print perp_value_3gram

