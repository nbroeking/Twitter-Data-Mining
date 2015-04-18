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

#Used to Iterate the cursor
def ResultIter(cursor, arraysize=1000):
    'An iterator that uses fetchmany to keep memory usage down'
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        for result in results:
            yield result

#Globals
word_features = []

#Feature Extration
def get_letters(tweets):
    features = []
    for (words, sentiment) in tweets:    
        features.extend(words)
    return features

#getFeatures
def get_features(wordlist):
    global word_features
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

#extract the features from the feture list
def extract_features(document):
    global word_features
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
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
    for x in lines:
        i+=1;
        line = x.split(",")
        if len(line) is 4:
            text = line[3].split()
            #Process the text
            newtext = []
            for word in text:
                if '@' in word:
                    newtext.append( 'TAG')
                elif 'http' in word:
                    newtext.append('URL')
                elif word.isalnum() and not len(word) < 3:
                    newtext.append(word)
            tup = (newtext, 'pos' if int(line[1]) else 'neg')
            if i < 10:
                trainingdata.append(tup)
            elif i < 100:
                testingdata.append(tup)
            else:
                break


    print('  Performing Feature extraction')
    #Feature extraction
    word_features = get_features(get_letters(trainingdata))


    print('  Applying the features to the classifer')
    #Feature application

    training_set = nltk.classify.util.apply_features(extract_features, trainingdata)

    classifier = nltk.NaiveBayesClassifier.train(training_set)

    print("Accuracy:")
    testing_set = nltk.classify.util.apply_features(extract_features, testingdata)
    print(nltk.classify.accuracy(classifier, testing_set))
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

            f.write("%d, %s, %r, %d, %s, %d, %d\n" % (row[0], classifier.classify(extract_features(row[1].split())), row[2], row[3], row[4], row[5], row[6])) 

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

    print ("Difference is %d" % ((datetime.datetime.now() - start).seconds))
