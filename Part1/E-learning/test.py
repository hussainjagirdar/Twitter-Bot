import string
import enchant
from langdetect import detect
from nltk.tokenize import word_tokenize

tokenList=[]
stopwords=['','(',')','{','}','\\','--',':']

fp =open("database.txt","r")
line=fp.readline()
print line

index=0
'''
while line:
    try:
        if detect(line.decode('utf-8').strip())=='en':
            tokens=[w.strip(string.punctuation).lower() for w in word_tokenize(line)]
            tokens=[w for w in tokens if not w in stopwords]
            tokenList.append('<s>')
            tokenList.extend(tokens)
            tokenList.append('</s>')
            print index
        line=fp.readline()
        index+=1
    except:
        line=fp.readline()
        continue
'''         

while line:
    tokens=[w.strip(string.punctuation).lower() for w in word_tokenize(line)]
    tokens=[w for w in tokens if not w in stopwords]
    tokenList.append('<s>')
    tokenList.extend(tokens)
    tokenList.append('</s>')
    line=fp.readline()
    index+=1
    if index%1000==0:
        print index


'''
while line:
	if detect(line.decode('utf-8').strip())=='en':
            tokens=[w.strip(string.punctuation).lower() for w in word_tokenize(line)]
            tokens=[w for w in tokens if not w in stopwords]
            tokenList.extend(tokens)
            print tokenList
    else:
            line=fp.readline()
            '''