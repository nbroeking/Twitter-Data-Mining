#Train the classifier
def train():
    global word_features

    f = open('training.csv')
    lines = f.read().splitlines()
    
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

            word_features.update(featureVec)

            tup = (text, 'pos' if int(line[1]) == 1 else 'neg')
            
            if i <= 20000:
                if( needPos and tup[1] == 'pos'):
                    trainingdata.append(tup)
                    needPos = False
                    i+=1;

                if( (needPos is False) and tup[1] == 'neg'):
                    trainingdata.append(tup)
                    needPos = True         
                    i+=1;

            elif i <= 100000:
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

    training_set = nltk.classify.util.apply_features(
                    extractFeatures, 
                    trainingdata)

    classifier = nltk.NaiveBayesClassifier.train(training_set)

    testing_set = nltk.classify.util.apply_features(
                    extractFeatures,
                    testingdata)

    return classifier

