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
import sqlite3
import time

#JSON
import json
import ast

#Globals
word_features = []

#Feature Extration
def get_words(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

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
        i+= 1
        #if i > 1000:
            #break

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
            #if i < 500000:
            trainingdata.append(tup)
            #else:
            #    testingdata.append(tup)
         
    print('  Performing Feature extraction')
    #Feature extraction
    word_features = get_features(get_words(trainingdata))

    print('  Applying the features to the classifer')
    #Feature application
    training_set = nltk.classify.util.apply_features(extract_features, trainingdata)
    
    return nltk.NaiveBayesClassifier.train(training_set)

#Main Function
if __name__ == '__main__':
    #Training the data
    print ("Training the Classifier")

    start = datetime.datetime.now()
    classifier = train()

    #Clasifying the database text
    print ("Classifying the database")

    #Testing
    text = ["I love hot dogs", "google sucks", "Apple is the best company", "why doesnt this work", "I really hate gas prices"]

    #print(classifier.show_most_informative_features(30))

    for x in text:
        print("%s: %s" % (x, classifier.classify(extract_features(x.split()))))

    print ("Difference is %d" % ((datetime.datetime.now() - start).seconds))
