#!/usr/bin/python2.7

#Future
from __future__ import absolute_import, print_function

#Imports sys to change path
import sys

#database
import sqlite3
import time

#THis is ugly but were just going to create the database right h
db = sqlite3.connect('Twitter.db')
# Get a cursor object
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Tweets(id INTEGER PRIMARY KEY, name TEXT, geo TEXT, image TEXT, source TEXT, timestamp TEXT, text TEXT, rt INTEGER)''')
db.commit()


sys.path.insert(1,'/home/nbroeking/DataMining/tweepy')
sys.path.insert(1,'/home/nbroeking//DataMining/loot/dist-packages')
#Import Tweepy

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#JSON
import json

# Consumer Keys
consumer_key="44vVVicDrIDrA9iJ6FHCUA0TB"
consumer_secret="tyeyRqSJkHrUjec2sdO5tiIJeMb5Sk5OZVySeN9CIEoXOFcvtn"

access_token="52314456-zHY3UfyiQ6KVrWrgMLy4nGmPzInaFmxsZVXhKCHfO"
access_token_secret="zYsjeIH7TKxeJnHxVHwg3HVUynu4JZgKLvfhsUR0Hn7Qh"

#Listen for tweets
class StdOutListener(StreamListener):
    def on_data(self, data):
	
	cursor.execute('''INSERT INTO MyTable(name, geo, image, source, timestamp, text, rt) VALUES(?,?,?,?,?,?,?)''',(tweet.user.screen_name, str(tweet.geo), tweet.user.profile_image_url, tweet.source, tweet.created_at, tweet.text, tweet.retweet_count))
        return True

    def on_error(self, status):
        print(status)

#Main Function
if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=['google'])
