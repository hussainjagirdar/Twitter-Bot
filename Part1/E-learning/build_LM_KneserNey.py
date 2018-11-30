#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 01:04:33 2018

@author: hussain
"""


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

print "tokens generated",len(tokens)
def n_grams():
    unigram=[w.lower() for w in train_corpus]
    bigram =[a for a in ngrams(unigram,2)]
    trigram =[a for a in ngrams(unigram,3)]
    return unigram, bigram, trigram

unigram, bigram, trigram = n_grams()

freq_1gram = nltk.FreqDist(train_corpus)
len_brown = len(train_corpus)
vocab=len(set(train_corpus))

def unigram_prob(word):
    return freq_1gram[ word] / len_brown
cfreq_2gram = nltk.ConditionalFreqDist(nltk.bigrams(tokens))
cprob_2gram = nltk.ConditionalProbDist(cfreq_2gram, nltk.SimpleGoodTuringProbDist)
 
def bigram_prob(word1, word2):
    return cprob_2gram[word1].prob(word2)

trigrams_as_bigrams=[]
trigram =[a for a in ngrams(train_corpus,3,pad_left=True,pad_right=True,left_pad_symbol='<s>', right_pad_symbol="</s>")]

cprob_kneser_3gram=nltk.KneserNeyProbDist(nltk.FreqDist(trigram))
 
def trigram_kneser(w1,w2,w3):
    return cprob_kneser_3gram.prob((w1,w2,w3)) 

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
        p=trigram_kneser(context[0], context[1], word)
    if p==0:
        return 0
    return -p*math.log(p , 2)

#logprob('at', ['smile'])

def perplexity(n, text):
      return pow(2.0, entropy(n, text))

entropy_value_3gram=entropy(3, test_corpus)
print entropy_value_3gram

perp_value_3gram=perplexity(3, test_corpus)
print perp_value_3gram