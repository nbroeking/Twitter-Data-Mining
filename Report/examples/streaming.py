def on_data(self, data):
    broadcast_sock.sendto(data, to_addr)
    d = json.loads(data.strip())
    try:
        if d['lang'] == "en":	
            cursor = self.db.cursor()
        
            cursor.execute('INSERT INTO Tweets( text, 
                retweeted, retweeted_count, 
                time, userid, tweetId) 
                VALUES(?,?,?,?,?,?)', 
                [d['text'], bool(d['retweeted']), 
                int(d['retweet_count']), 
                d['created_at'], int(d['user']['id']), 
                int( d['id'])])
            
            cursor.execute('INSERT INTO Users( userID, 
                followers_count, friendcount, 
                name) VALUES (?,?,?,?)', 
                [d['user']['id'], 
                d['user']['followers_count'], 
                d['user']['friends_count'], 
                d['user']['name']])
        
            self.db.commit()
            return True

    except: # catch *all* exceptions
        e = sys.exc_info()[0]
        print( e )


