import nltk
import string
from nltk.util import ngrams
#stopwords=['','(',')','{','}','\\','--',':']

corpus=nltk.corpus.brown
print corpus.words()[:50]

tokens=[w.strip(string.punctuation).lower() for w in corpus.words()]
print tokens
#tokens=[w for w in tokens if not w in stopwords]

spl =int(95*len(tokens)/100)
train_corpus = tokens[:spl]
test_corpus = tokens[spl:]

freq_1gram = nltk.FreqDist(train_corpus)
len_brown = len(train_corpus)

print len_brown

def unigram_prob(word):
    return freq_1gram[ word] / len_brown

print nltk.bigrams(tokens)

cfreq_2gram = nltk.ConditionalFreqDist(nltk.bigrams(tokens))
cprob_2gram = nltk.ConditionalProbDist(cfreq_2gram, nltk.MLEProbDist)

def bigram_prob(word1, word2):
    return cprob_2gram[word1].prob(word2)

#cprob_2gram["betting"].prob("men")
#bigram_prob("betting","men")

trigrams_as_bigrams=[]
trigram =[a for a in ngrams(train_corpus,3,pad_left=True,pad_right=True,left_pad_symbol='<s>', right_pad_symbol="</s>")]
trigrams_as_bigrams.extend([((t[0],t[1]), t[2]) for t in trigram])
cfreq_3gram = nltk.ConditionalFreqDist(trigrams_as_bigrams)
cprob_3gram = nltk.ConditionalProbDist(cfreq_3gram, nltk.MLEProbDist)

def trigram_prob(w1, w2, w3):
   return cprob_3gram[(w1, w2)].prob(w3)

#cprob_3gram['than','three'].samples()

"""
LaplaceProbDist
SimpleGoodTuringProbDist
KneserNeyProbDist
"""
#prob=trigram_prob('general', 'election', 'ballot')

def bigram_prob_with_add1smoothing(word1, word2):
    cprob_2gram_add1=float((((1+cfreq_2gram[word1][word2])/(len(cfreq_2gram)+sum(cfreq_2gram[word1].values())))))
    return cprob_2gram_add1
    
def trigram_prob_with_add1smoothing(w1, w2, w3):
    cprob_3gram_add1=float((((1+cfreq_3gram[(w1,w2)][w3])/(len(cfreq_3gram)+sum(cfreq_3gram[(w1,w2)].values())))))
    return cprob_3gram_add1

#P(how do you do) = P(how) * P(do|how) * P(you|do) * P(do | you)
# how do hggh do
#prob_sentence = unigram_prob("how") * bigram_prob("how","do") * bigram_prob("do","you") * bigram_prob("you","do")
#cprob_2gram['my'].generate()
#The grand jury commented on a number of other topics

#prob_sent=unigram_prob("the") * bigram_prob('the', 'grand') * bigram_prob('grand', 'jury') * bigram_prob('jury', 'commented') * bigram_prob('commented', 'on') * bigram_prob('commented', 'on') * bigram_prob('on', 'a') * bigram_prob('a', 'number') * bigram_prob('number', 'of') * bigram_prob('of', 'other') * bigram_prob('other', 'topics')



#('the','fulton')