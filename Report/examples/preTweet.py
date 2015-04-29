#start replaceTwoOrMore
def replaceTwoOrMore(s):
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)

#Preprocess the tweet
def PreprocessTweet(tweet):
    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|
        (https?://[^\s]+))','URL',tweet)

    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','USER',tweet)

    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)

    #Replace hashtag with the word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)

    #trim
    tweet = tweet.strip('\'"')

    return tweet

