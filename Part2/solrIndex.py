import simplejson as json
import requests
from nltk.util import ngrams
from tokenizer import tokenizer
import timeit

#Using tweet tokenizer (not of nltk)
T = tokenizer.TweetTokenizer(preserve_handles=False, preserve_hashes=False, preserve_case=False, preserve_url=False)

try:
    count=0;
    unidata = [ ]
    bidata = []
    bigrams = dict()

    with open("../Assignment1/E-learning/final_data.txt") as corpusFile:
        for tweet in corpusFile:
            tokens=T.tokenize(tweet)
            bgrams=list(ngrams(tokens,2))
		
		#Updating Dictionaries
            for words in bgrams:
                key=words[0]+"@#,"+words[1]
                if(bigrams.has_key(key)):
                    bigrams[key]+=1
                else:
                    bigrams[key]=1

            count+=1
		
		#Indexing dictionaries after every 10000 bigrams altogether.
            if count%10000 ==0:
                for key, value in bigrams.iteritems():
                    bi=key.split("@#,")
                    first=bi[0]
                    second=bi[1]
                    bidata.append( {"id":key,"first":first,"second":second,"count":{"inc":value}} )
		# Updates a single field in a document with id 'doc_id'.

	    	base_url = 'http://localhost:8983/'
	    	solr_url = 'solr/bigram_core/'
    		update_url = 'update?commit=true'
    		full_url = base_url + solr_url + update_url
    		headers = {'content-type': "application/json"}

	    	response = requests.post(full_url, data=json.dumps(bidata), headers=headers)

                try:
                    response.raise_for_status()
                except requests.exceptions.HTTPError as e:
                    print "Error: " + str(e)

                bidata=[]
                bigrams=dict()

                print "...{0} tweets indexed.".format(count)

except Exception as e:
    print(e)

