def convertDatabase(classifier):
    fapple = open('results/apple.csv','w')
    google = open('results/google.csv','w')
    samsung = open('results/samsung.csv','w')
    amazon = open('results/amazon.csv', 'w')
 
    try:
        con = lite.connect(sys.argv[1])
    
        cur = con.cursor()    
        cur.execute('SELECT Tweets.id, text, retweeted, 
                    retweeted_count, time, 
                    followers_count, 
                    friendcount from Tweets LEFT JOIN Users on 
                    Tweets.userid == Users.userid 
                    group by Tweets.id;');
   
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

            f.write("%d, %s, %r, %d, %s, %d, %d\n" % (row[0], 
                classifier.classify(
                    extractFeatures(
                        getFeatureVector(PreprocessTweet(row[1])))),
                row[2], row[3], 
                row[4], row[5], 
                row[6])) 

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


