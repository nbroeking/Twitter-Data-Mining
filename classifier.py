#!/usr/bin/python2.7

#Future
from __future__ import absolute_import, print_function

#Imports sys to change path
import sys

#Classifier
import re, math, collections, itertools
import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist

#time
import datetime

#database
import sqlite3 as lite
import time

#JSON
import json
import ast

#We need regular expressions
import re

#Globals
word_features = []
stopWords = []

#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)

#start getStopWordList
def getStopWordList():
    #read the stopwords file and build a list
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fp = open("stopwords.txt", 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords


stopWords = getStopWordList()

#start getfeatureVector
def getFeatureVector(tweet):
    featureVector = []
    #split tweet into words
    words = tweet.split()
    for w in words:

        #replace two or more with two occurrences
        #We want to keep repeted letters because people use it to show emphasis
        w = replaceTwoOrMore(w)

        #strip punctuation from the tweets
        w = w.strip('\'"?,.')

        #check if the word starts with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)

        #ignore if it is a stop word
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())

    return featureVector

#Preprocess the tweet
def PreprocessTweet(tweet):
    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace hashtag with the word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')

    return tweet

#Used to Iterate the cursor
def ResultIter(cursor, arraysize=1000):
    'An iterator that uses fetchmany to keep memory usage down'
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        for result in results:
            yield result

#start extract_features
def extractFeatures(tweet):
    global word_features
    words = set(tweet)
    features = {}
    for word in word_features:
        #features['contains(%s)' % word] = (word in words)
        features[word] = word in tweet
    #print('Extract Features')
    #print( features )
    #print('\n\n')
    return features

#Train the classifier
def train():
    global word_features

    f = open('training.csv')
    lines = f.read().splitlines()
    
    print('  Preparing the data')
    #Create a list of training data
    trainingdata = []
    testingdata = []
    i = 0
    needPos = True
    for x in lines:
        line = x.split(",")

        #If we have a good formed data string
        if len(line) is 4:

            text = PreprocessTweet(line[3])
            featureVec = getFeatureVector(text)

            word_features.extend(featureVec)

            tup = (text, 'pos' if int(line[1]) == 1 else 'neg')
            
            if i <= 13000:
                if( needPos and tup[1] == 'pos'):
                    trainingdata.append(tup)
                    needPos = False
                    i+=1;

                if( (needPos is False) and tup[1] == 'neg'):
                    trainingdata.append(tup)
                    needPos = True         
                    i+=1;

            elif i <= 20000:
                if( needPos and tup[1] == 'pos'):
                    testingdata.append(tup)
                    needPos = False
                    i+=1;

                if( (needPos is False) and tup[1] == 'neg'):
                    testingdata.append(tup)
                    needPos = True         
                    i+=1;
            else:
                break


    print('  Performing Feature extraction')
    #Feature extraction

    #We want to remove duplicates
    word_features = list(set(word_features))

    print('  Applying the features to the classifer')
    #Feature application

    training_set = nltk.classify.util.apply_features(extractFeatures, trainingdata)
    classifier = nltk.NaiveBayesClassifier.train(training_set)

    print('   Applying features to testing data')

    #testing_set = nltk.classify.util.apply_features(extractFeatures, testingdata)

   # print("Accuracy:")
    #print(nltk.classify.accuracy(classifier, testing_set))
    #print(nltk.classify.accuracy(classifier, testing_set))
    return classifier

def convertDatabase(classifier):
    fapple = open('results/apple.csv','w')
    google = open('results/google.csv','w')
    samsung = open('results/samsung.csv','w')
    amazon = open('results/amazon.csv', 'w')
 
    try:
        con = lite.connect(sys.argv[1])
    
        cur = con.cursor()    
        cur.execute('SELECT Tweets.id, text, retweeted, retweeted_count, time, followers_count, friendcount from Tweets LEFT JOIN Users on Tweets.userid == Users.userid group by Tweets.id LIMIT 10;');
   
        f = fapple
        i = 0;
        for row in ResultIter(cur):
            i+=1
            if "apple" in row[1].lower():
                f = fapple
            if "google" in row[1].lower():
                f = google

            if "samsung" in row[1].lower():
                f = samsung

            if "amazon" in row[1].lower():
                f = amazon

            f.write("%d, %s, %r, %d, %s, %d, %d\n" % (row[0], classifier.classify(extractFeatures(getFeatureVector(PreprocessTweet(row[1])))), row[2], row[3], row[4], row[5], row[6])) 

            if i %100 == 0:
                print (i)

    except lite.Error, e:    
        print ( "Error %s:" % e.args[0])
        sys.exit(1)
    
    finally:
        if fapple:
            fapple.close()
        if google:
            google.close()
        if samsung:
            samsung.close()
        if amazon:
            amazon.close()    
        if con:
            con.close()

#Main Function
if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        print("Error: Usage");
        exit(0)
    #Training the data
    print ("Training the Classifier")

    start = datetime.datetime.now()
    classifier = train()

    #Clasifying the database text
    print ("Classifying the database")
    convertDatabase(classifier);

#    print('Enter Sentences')
 #   while True:
  #      userinput = sys.stdin.readline()
   #     print (classifier.classify(extractFeatures(getFeatureVector(PreprocessTweet(userinput)))))


    print ("Difference is %d" % ((datetime.datetime.now() - start).seconds))
