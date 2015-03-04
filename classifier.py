#!/usr/bin/python2.7

#Future
from __future__ import absolute_import, print_function

#Imports sys to change path
import sys

#database
import sqlite3
import time


sys.path.insert(1,'/home/nbroeking/DataMining/tweepy')
sys.path.insert(1,'/home/nbroeking//DataMining/loot/dist-packages')

#JSON
import json
import ast

def train():
    f = open('training.txt')
    lines = f.read().splitlines()
    
    #Create a list of training data
    data = []
    for x in lines:
        line = x.split("^")
        if len(line) is 2:
            data.append((line[0], line[1]))
         
      
    tweets = []  
    #format     
    for (words, sentiment) in data:
        words_filtered = [word.lower() for word in words.split() if len(word) >= 3\
        and word.isalpha()]
        tweets.append((words_filtered, sentiment))

    return tweets

        
#Main Function
if __name__ == '__main__':
    print ("Categorizing the data")
    tweets = train()
    
