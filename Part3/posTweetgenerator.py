import pysolr
import string
from random import randint
import nltk
tweetLength=10
punctuations=list(string.punctuation)
print "hello"
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

inputfile=open("wordlist","r")
outputfile=open("output","w")
#Taking keyword from the user.
keyword = inputfile.readline()
while keyword:
  print keyword
  keyword=keyword[:-1]
  #Making a pivot for keyword.
  pivot=randint(0,9)
  print "pivot=",pivot

  posTemplateList=[]
  f=open("someGoodSentences","r")
  while 1:
    #inputSentence=raw_input("Enter Sentence\n")
    inputSentence=f.readline()
    if inputSentence=="stop\n":
      break
    tempList=[]
    text=nltk.word_tokenize(inputSentence)
    posOutputList=nltk.pos_tag(text)
    #print posOutputList
    for item in posOutputList:
      tempList.append(item[1])
    posTemplateList.append(tempList)
  print posTemplateList
  f.close()

  tweetWordDictList=[]
  for template in posTemplateList:
    print "template=",template
    pivot=0
    posIndex=0
    tweetWordDict={}
    keylist=[]
    keylist.append(keyword)
    #print nltk.pos_tag(tlist)
    for pos in template:
      #print "pos=",pos
      #print "nltk.pos_tag(keylist)",nltk.pos_tag(keylist)[0][1]
      if pos!=nltk.pos_tag(keylist)[0][1]:
        posIndex+=1
        continue
      else:
        pivot=posIndex
        #print "pivot=",pivot
        break

    tweetWordDict[pivot]=keyword
    temp=keyword

    if posIndex==len(template):
      continue

    #Making right side of the template.
    for i in xrange(pivot+1,len(template)):
      results = solr.search('first:'+escapeSolrArg(temp),rows='1000',sort='count desc')
      if len(results)==0:
        i-=1
        continue
      index=0
      candidateList=[]
      for result in results:
        seclist=[]
        seclist.append(result["second"])
        if nltk.pos_tag(seclist)[0][1] != template[i]:
          continue
        elif nltk.pos_tag(seclist)[0][1] == template[i]:
         #temp=result["second"]
         #tweetWordDict[i]=result["second"]
         #break
         candidateList.append(result["second"])
        index+=1
      if len(candidateList)!=0:
        randNum=randint(0,len(candidateList)-1)
        temp=candidateList[randNum]
        tweetWordDict[i]=candidateList[randNum]


    #Making Left part of tweet.
    temp=keyword
    for i in xrange(pivot-1,0,-1):
      results = solr.search('second:'+escapeSolrArg(temp),rows='1000',sort='count desc')
      if len(results)==0:
        i-=1
        continue
      index=0
      candidateList=[]
      for result in results:
        firlist=[]
        firlist.append(result["first"])
        if nltk.pos_tag(firlist)[0][1] != template[i]:
          continue
        elif nltk.pos_tag(firlist)[0][1] == template[i]:
         #temp=result["first"]
         #tweetWordDict[i]=result["first"]
         #break
         candidateList.append(result["second"])
        index+=1
      if len(candidateList)!=0:
        randNum=randint(0,len(candidateList)-1)
        temp=candidateList[randNum]
        tweetWordDict[i]=candidateList[randNum]
    tweetWordDictList.append(tweetWordDict)

  for item in tweetWordDictList:
    print item
    for i in xrange(len(item)):
      if i+1 in item:
        outputfile.write(item[i+1]+" ")
    outputfile.write("\n")
  keyword=inputfile.readline()
  outputfile.write("-----------------------------")
  outputfile.write("\n")
inputfile.close()
outputfile.close()
