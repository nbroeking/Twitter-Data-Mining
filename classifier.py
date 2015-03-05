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

#database
import sqlite3
import time

#JSON
import json
import ast

def train():
    f = open('training.csv')
    lines = f.read().splitlines()
    
    #Create a list of training data
    trainingdata = []
    testingdata = []
    i = 0
    for x in lines:
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
            if i < 500000:
                trainingdata.append(tup)
            else:
                testingdata.append(tup)
         
    #Feature extraction


    #Clasification
   
 
    print (data)
      
#Main Function
if __name__ == '__main__':
    print ("Categorizing the data")
    tweets = train()
    
