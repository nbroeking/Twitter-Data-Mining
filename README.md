DESCRIPTION 
=========== 

In this project we created a sentiment analyzer that streams twitter collecting
tweets on keywords related to Apple, Google, Samsung, and Amazon. We then took
these tweets ran them through a Naive Bayes Classifier. We then took the
classification ran correlation analysis and determined that there is no
correlation between the two data sets. In addition to the analysis we also
created a real time sentiment engine. This engine creates a Rest Api that
allows remote devices to get real time sentiment analysis. To compliment the
api there is a android application that will reach out to the api and process
the information and display it to the user.

Report
------

The report, which includes key results and information is included in
Report.pdf. All resources used to create the report can be located in the sub
director Report.

Analysis
--------

The first stage of our process includes all code related to the correlation. 
This code can be found in the Analysis sub folder. It consists of several sections.

__*Streaming.py__
    This file has all the code that pulled tweets and stored them in our database.


