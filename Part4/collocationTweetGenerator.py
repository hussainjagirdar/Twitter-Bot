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

#Taking keyword from the user.
iline = inputfile.readline()
while iline:
  print iline
  keywordList =iline.split(" ")
  keyword1=keywordList[0]
  keyword2=keywordList[1][:-1]
  print "keyword1",keyword1
  print "type_keyword1",nltk.pos_tag(list(keyword1))[0][1]
  print "keyword2",keyword2
  print "type_keyword2",nltk.pos_tag(list(keyword2))[0][1]
  tweetWordDictList=[]
  for template in posTemplateList:
    print "template=",template
    pivot1=0
    pivot2=0
    posIndex=0
    tweetWordDict={}
    key1list=[]
    key1list.append(keyword1)

    #Finding pivot1 for first keyword.
    for pos in template:
      #print "pos=",pos
      #print "nltk.pos_tag(keylist)",nltk.pos_tag(keylist)[0][1]
      if pos!=nltk.pos_tag(key1list)[0][1]:
        posIndex+=1
        continue
      else:
        print "key1",nltk.pos_tag(key1list)[0][1]
        pivot1=posIndex
        #print "pivot=",pivot
        break
    tweetWordDict[pivot1]=keyword1
    #Checking if keyword are found or not
    if pivot1==0:
      continue

    #Finding pivot2 for second keyword.
    posIndex=0
    key2list=[]
    key2list.append(keyword2)
    for z in xrange(pivot1+1,len(template)):
      if template[z]!=nltk.pos_tag(key2list)[0][1]:
        posIndex+=1
      else:
        print "key2",nltk.pos_tag(key2list)[0][1]
        pivot2=z
        break
    tweetWordDict[pivot2]=keyword2
    print "pivot1",pivot1
    print "pivot2",pivot2

    #Checking if keyword are found or not
    if pivot2==0:
      continue
    '''
    #Finding pivot2 for second keyword.
    posIndex=0
    for pos in template:
      if pos!=nltk.pos_tag(key1list)[0][1] or pos==pivot1:
        posIndex+=1
        continue
      else:
        pivot2=posIndex
        #print "pivot=",pivot
        break
    tweetWordDict[pivot2]=keyword2
    '''

    #Finding Bi-grams from solr.
    temp=keyword1

    #Making right side of the template of keyword1.
    for i in xrange(pivot1+1,pivot2):
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


    #Making Left part of tweet of keyword1.
    temp=keyword1
    for i in xrange(pivot1-1,0,-1):
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


    #Making right side of the template of keyword1.
    temp=keyword2
    for i in xrange(pivot2+1,len(template)):
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
  for item in tweetWordDictList:
    print item
    for i in xrange(len(item)):
      if i+1 in item:
        outputfile.write(item[i+1]+" ")
    outputfile.write("\n")
  iline=inputfile.readline()
  outputfile.write("-----------------------------")
  outputfile.write("\n")
inputfile.close()
outputfile.close()

  
#########################################################################
