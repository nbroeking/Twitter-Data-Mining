#start extract_features
def extractFeatures(tweet):

    if not isinstance(tweet, list):
        tweet = tweet.split(' ')

    class default_dict(dict):
        def __init__(self):
            super(default_dict, 
            self).__init__()
        
        def __getitem__(self, k):
            self.get(k, False)

    features = default_dict()

    for word in tweet:
        if word in word_features:
            features[word] = True

    return features

