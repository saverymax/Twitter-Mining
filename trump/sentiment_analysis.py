from textblob import TextBlob
import re

class process_tweet():
    """Clean tweet and analyze text"""

    def __init__(self):
        """initiate instance of tweet text to be analyzed""" 
        pass

    def filter_tweet(self, tweet_dataframe)
        for row in tweet_dataframe:
            #clean tweet

    def process_sentiment(self, tweet_dataframe):
        for tweet in tweet_dataframe:
            analysis = TextBlow(tweet)
            #analyze sentiment

data['SA'] = np.array([ analize_sentiment(tweet) for tweet in data['Tweets'] ])
