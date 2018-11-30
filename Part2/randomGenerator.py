import pysolr
import string
from random import randint
tweetLength=10
punctuations=list(string.punctuation)

# escaping doesn't matter
escapeRules = {'+': r'\+',
               '-': r'\-',
               '&': r'\&',
               '|': r'\|',
               '!': r'\!',
               '(': r'\(',
               ')': r'\)',
               '{': r'\{',
               '}': r'\}',
               '[': r'\[',
               ']': r'\]',
               '^': r'\^',
               '~': r'\~',
               '*': r'\*',
               '?': r'\?',
               ':': r'\:',
               '"': r'\"',
               ';': r'\;',
               ' ': r'\ '}

def escapedSeq(term):
    """ Yield the next string based on the
        next character (either this char
        or escaped version """
    for char in term:
        if char in escapeRules.keys():
            yield escapeRules[char]
        else:
            yield char

def escapeSolrArg(term):
    """ Apply escaping to the passed in query terms
        escaping special characters like : , etc"""
    term = term.replace('\\', r'\\')   # escape \ first
    return "".join([nextStr for nextStr in escapedSeq(term)])


# Setup a Solr instance. The timeout is optional.
solr = pysolr.Solr('http://localhost:8983/solr/bigram_core/', timeout=10)

#Taking keyword from the user.
keyword = raw_input("Enter the word\n")

#Making a pivot for keyword.
pivot=randint(0,9)
print "pivot=",pivot

tweetWordDict={}
tweetWordDict[pivot]=keyword
temp=keyword
#Making Right part of tweet.
for i in xrange(pivot+1,tweetLength+1):
	results = solr.search('first:'+escapeSolrArg(temp),rows='100',sort='count desc')
	if len(results)==0:
		i-=1
		continue
	randNum=randint(0,len(results))
	index=0
	for result in results:
		if result["second"] in punctuations:
			continue
		if index==randNum:
			temp=result["second"]
			tweetWordDict[i]=result["second"]
			break
		index+=1


temp=keyword
#Making Left part of tweet.
for i in xrange(pivot-1,0,-1):
	results = solr.search('second:'+escapeSolrArg(temp),rows='100',sort='count desc')
	if len(results)==0:
		i-=1
		continue
	randNum=randint(0,len(results))
	index=0
	for result in results:
		if result["first"] in punctuations:
			continue
		if index==randNum:
			temp=result["first"]
			tweetWordDict[i]=result["first"]
			break
		index+=1

print tweetWordDict
