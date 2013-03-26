# -*- coding ntf-8 -*-
# ***************************************************************************
# This is the homework2 for social media in cuhk
# which trains some SVM classifiers
# Now the code need to modify the parameters to suit the experiments MANUALLY
# ***************************************************************************
from __future__ import division
from string import punctuation
import re,nltk,math,string
#import nltk
#import math

def combineList(list):
    # combine each line to a list            
    feature = []            
    for x in list:
        feature = x + feature
                   
    return feature

#start preProcessLine
def preProcessLine(line):
    #low case
    #import ipdb; ipdb.set_trace()
    line = line.lower()
    #remove additional white space
    line = re.sub('[\s]+', ' ', line)
    
    #remove punctuations
    for p in list(punctuation):
        line = line.replace(p, '')

    #word stemming    
    #wordStemming()
    # Now we use the script PStemmer.py
    wordFiltered = []
    words = line.split()
    for w in words:
        
        #strip punctuation
        w = w.strip('\'"?,.')
        #if the word starts with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$",w)
       
        #ignore it if it is a stop word
        if (w in stopWords or val is None):
            continue
        else:
            #only lenth of word is larger than two
            word = [e.lower() for e in w.split() if len(e) >= 2] 
            if (len(word) != 0):
                wordFiltered.append(word)

                #mapWordsToIDs(wordFiltered) 
    feature = combineList(wordFiltered)
        #mapWordsToIDs(feature)    
    
    return feature
#end
    
#start getStopWordList
def getStopWordList(file):
    #build a list for stop words
    stopWords = []
    fp = open(file, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()

    return stopWords
#end

#start mapWordsToIDs
def mapWordsToIDs(sentences):
    dict = {}      

    for i, word in enumerate(sentences):
        dict[word] = i+1
       
    return dict
        
#end
'''
#start genFeature
def genFeature(line):
    #function:get the feature and map words to ID
    
    #list feature is used to store words in each line(review)
    feature = []
    # wordId stores the unique id for each word    
    #wordId = 1    
    #split line(review) into words
    words = line.split()
    for w in words:
        
        #strip punctuation
        w = w.strip('\'"?,.')
        #if the word starts with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$",w)
        #ignore it if it is a stop word
        #print stopWords
        if (w in stopWords or val is None):
            continue
        else:
            wordFiltered = [e.lower() for e in w.split() if len(e) >= 2]
            feature.append(wordFiltered)
            #import ipdb; ipdb.set_trace()
            
            #wordDict[wordFiltered] = wordId
            
    return feature
#end
'''
#start getTop2000Words
def getTop2000Words(list):
    #frequency distribution
    listFreq = nltk.FreqDist(list)
    #in decreasing order of frequency
    vocabulary = listFreq.keys()
    #print  vocabulary[:6]
    return vocabulary[:2000]
#end

def numWordInArray(array,word):
    k = 0
    #each document(line)
    #print("word:",word)
    for doc in array:
        #each word
        #for item in doc:
       
            if word in doc :
                
                k += 1
                #print("k:",k)
    return k

#start generateUnigramFeature
def generateUnigramFeatures(posSentences, negSentences):
    # number of document
    n = len(posSentences + negSentences)
    if ( termWeight == 1):
        #the below two lsit is used to store the norm freq 
        posNormFreq = {}
        negNormFreq = {} 
            
    if ( termWeight == 2):
        #the two list store the tf-IDF
        posTfIdf = {}
        negTfIdf = {}  
          
    for i in posSentences:
        posWords = preProcessLine(i)
        features = [posWords, +1]    
        posFeatures.append(features)
        #print posFeatures

        #each words in each line(review)
        #posFeatures = [featureSelect(posWords), 1]
        
        for word in posWords:
            if termWeight == 1:
               
                # Normalized Freq.
                normFreq = posWords.count(word) / len(posWords)
                #posNormFreq.append(normFreq)

                posNormFreq[word] = normFreq
           
            elif termWeight == 2:            
                # term frequency
                tf = posWords.count(word)

                # document frequency
                df = numWordInArray( posSentences + negSentences, word)
                #something the there are some wrong words, like middle-earth becomes middleearth
                if df == 0:
                    df += 1

                #print("posidf:",idf)
                tfidf = tf * math.log10(n/df)
                #print("tfidf:",tfidf)
                posTfIdf[word] = tfidf
                
            else:
                print("error")
                        
    for i in negSentences:
        negWords = preProcessLine(i)
        features = [negWords, -1]
                
        negFeatures.append(features) 
        #print negFeatures
        
        for word in negWords:
            #normalized Freq.
            if termWeight == 1:
                normFreq = negWords.count(word) / len(negWords)

                negNormFreq[word] = normFreq
                #negNormFreq.append(normFreq)
                    
            elif termWeight == 2:
               # term frequency
                tf = negWords.count(word)
                # document frequency
                df = numWordInArray(posSentences + negSentences, word)
                if df == 0:
                    df += 1
                #print("df-neg:",df)

                #idf = math.log10(n/df)
                #print("negidf:",idf)
                tfidf = tf * math.log10(n/df)
                #print("tfidf-neg:",tfidf)

                negTfIdf[word] = tfidf
            else:
                print("error")
        
    if termWeight == 1:
        #print posNormFreq 
        #print negNormFreq
        return  {'posNormFreq':posNormFreq, 'negNormFreq':negNormFreq}
    if termWeight == 2:
        #print posTfIdf + negTfIdf
        return  {'posTfIdf':posTfIdf, 'negTfIdf':negTfIdf}
         
#end
    
#start preProcess
def process():
    #data pre-processing
    negSentences = open(sourceDir+negFile, 'r')
    posSentences = open(sourceDir+posFile, 'r')
    
    posSentences = re.split(r'\n',posSentences.read())
    negSentences = re.split(r'\n',negSentences.read())

    allWords = []
    #map the word with unique id
    for i in posSentences + negSentences :
        words = preProcessLine(i)
        allWords.extend(words)
        
    #print allWords
    #whether top 2000 words
    #topword = 1
    if topword == 1:
        top2000Words = getTop2000Words(allWords)
        wordId = mapWordsToIDs(top2000Words)
    else:
        wordId = mapWordsToIDs(allWords)

        #print wordId
    
    # TF-IDF or Normalized Freq.
    #termWeight = 1
    dict = generateUnigramFeatures(posSentences, negSentences)
    if ( termWeight == 1):
        posResult = dict['posNormFreq']
        negResult = dict['negNormFreq']
        
    if ( termWeight == 2):
        posResult = dict['posTfIdf']
        negResult = dict['negTfIdf']
    
        #print posResult 
        #print negResult   
    #select 4/5 of the features to be used for training and 1/5 to be used for testing

    posCutoff1 = int(math.floor(len(posFeatures)*1/5))
    negCutoff1 = int(math.floor(len(negFeatures)*1/5))

    posCutoff2 = int(math.floor(len(posFeatures)*2/5))
    negCutoff2 = int(math.floor(len(negFeatures)*2/5))

    posCutoff3 = int(math.floor(len(posFeatures)*3/5))
    negCutoff3 = int(math.floor(len(negFeatures)*3/5))

    posCutoff4 = int(math.floor(len(posFeatures)*4/5))
    negCutoff4 = int(math.floor(len(negFeatures)*4/5))

    # The next defines the train data set and test data set
    # Todo: it is better do it automatically
    #test for 4/5 -5/5
    trainFeatures = posFeatures[:posCutoff4] + negFeatures[:negCutoff4] 
        #print trainFeatures
    testFeatures = posFeatures[posCutoff4:] + negFeatures[negCutoff4:]

    '''
    #test for 3/5-4/5
    trainFeatures = posFeatures[:posCutoff3] + negFeatures[:negCutoff3] + posFeatures[posCutoff4:len(posFeatures)] + negFeatures[negCutoff4:len(negFeatures)]
    #print trainFeatures
    testFeatures = posFeatures[posCutoff3:posCutoff4] + negFeatures[negCutoff3:negCutoff4]
    '''
    #test for 2/5-3/5 
    '''
    trainFeatures = posFeatures[:posCutoff2] + negFeatures[:negCutoff2] + posFeatures[posCutoff3:len(posFeatures)] + negFeatures[negCutoff3:len(negFeatures)]
    #print trainFeatures
    testFeatures = posFeatures[posCutoff2:posCutoff3] + negFeatures[negCutoff2:negCutoff3]
    '''
    '''
    #test for 1/5-2/5 
    trainFeatures = posFeatures[:posCutoff1] + negFeatures[:negCutoff1] + posFeatures[posCutoff2:len(posFeatures)] + negFeatures[negCutoff2:len(negFeatures)]
    #print trainFeatures
    testFeatures = posFeatures[posCutoff1:posCutoff2] + negFeatures[negCutoff1:negCutoff2]
    '''
    '''
    #test for 0-1/5 
    trainFeatures = posFeatures[posCutoff1:len(posFeatures)] + negFeatures[negCutoff1:len(negFeatures)]

    testFeatures = posFeatures[:posCutoff1] + negFeatures[:negCutoff1]
    '''
    #print trainFeatures
    #print testFeatures
    #write file for svm analysis
    trainingfo = open(targetDir + trainingData, 'w')
    testingfo = open(targetDir + testingData, 'w')
    
    for (words, sentiment) in trainFeatures:
       
         #according to SVMlight, Features should be in increasing order,so
        dict = {}
        wordsbyValue = []
        if len(words) != 0:    
            for word in words:
                # if only top words, some words doesn't exist in dict wordId
                # 
                if topword == 1:
                    if word in wordId:
                        dict[word] = wordId[word]    
                    else:
                        continue
                else:
                    dict[word] = wordId[word]
                                
                #value is in increasing order
                #in top words modle, dict might be null, so,
            if len(dict) != 0:
                key,value = zip(*[(key,dict[key]) for key in sorted(dict,key=dict.get)])
                wordsbyValue = list(key)
        
                #print wordsbyValue
            line = str(sentiment)
        
            for word in wordsbyValue:
                    
                if sentiment == 1:
                    
                    element = str(wordId[word]) + ":" + str(posResult[word])
                if sentiment == -1:
                    element = str(wordId[word]) + ":" + str(negResult[word])
                
                line = line + " " + element
                #print line
            trainingfo.write(line + "\n")
            
    for (words, sentiment) in testFeatures:
        
        #according to SVMlight, Features should be in increasing order,so
        dict = {}
        wordsbyValue = []
        if len(words) != 0:    
            for word in words:
                if topword == 1:
                    if word in wordId:
                        dict[word] = wordId[word]    
                    else:
                        continue
                else:
                    dict[word] = wordId[word]
        
            if len(dict) != 0:
            #value is in increasing order
                key,value = zip(*[(key,dict[key]) for key in sorted(dict,key=dict.get)])
                wordsbyValue = list(key)
        
            #print wordsbyValue
            line = str(sentiment)
        
            for word in wordsbyValue:
                    
                if sentiment == 1:
                   
                    #print str(wordId[word])
                    #print str(posResult[word])
                    element = str(wordId[word]) + ":" + str(posResult[word])
                if sentiment == -1:
                    element = str(wordId[word]) + ":" + str(negResult[word])
                #print element
                line = line + " " + element
            print line
            testingfo.write(line + "\n")
        
    trainingfo.close()
    testingfo.close()
    #
#end

#begin main
if __name__ == "__main__":
    #init variable
    sourceDir="/home/zhaowenlong/workspace/class/social_media/source/"
    stopFile="stopwords.txt"
    stopWords = getStopWordList(sourceDir+stopFile)
    #files = ['polarity.neg', 'polarity.pos']
    negFile="polarity.neg"
    posFile="polarity.pos"

    targetDir = "/home/zhaowenlong/workspace/class/social_media/1155011105_assign2/experiments/fold1/"
    trainingData = "training_exp1_f1.dat"
    testingData  = "testing_exp1_f1.dat"
    model = "model_exp1_f2"
    '''
    svm_learn = "/home/zhaowenlong/workspace/lib/svm_light/svm_learn"
    svm_classify = "/home/zhaowenlong/workspace/lib/svm_light/svm_classify"

    import commands
    commands.getstatusoutput("svm_learn targetDir+trainingData targetDir+model_exp1_f2") 
    commands.getstatusoutput("svm_classify targetDir+testingData targetDir+predictions")
    '''
    #processing
    #
    #Global variable, used to store the features
    posFeatures = []
    negFeatures = []
    # termWeight determines Normalized Freq (default) or TF-IDF
    termWeight = 1
    #topword defines whether use top 2000 words function
    # default is off
    topword = 0
    
    #begin
    process()

    
