#!/usr/bin/env python3
from textblob import TextBlob
import argparse
import re
import string
import pandas as pd
import os
from nltk.stem import WordNetLemmatizer as WNL

"""
Sentiment analysis on time series data
Call from commandline: python sentiment_analysis.py --file file.tsv
"""

def get_parser():
    """
    Set up command line options. In this script, the filename of the tsv to be read must be given. Include file extension. 
    Documentation: 
    docs.python.org/2/library/argparse.html 
    """

    parser = argparse.ArgumentParser(description = "Twitter stream") 
    parser.add_argument("--file", 
                        dest = "filename", 
                        help = "The file to be analyzed")
    return parser

class process_tweet():
    """Clean tweet and analyze text"""

    def __init__(self, tweet_dataframe, filename):
        """initiate instance of tweet text to be analyzed""" 
         
        self.tweet_dataframe = tweet_dataframe
        self.filename = filename

    def filter_tweet(self):
        """Remove chosen elements from tweets. Depending on hardcoded values, this might be hashtags, @mentions, urls, or all non-alphanumeric characters."""
        # need to change all cases
        excess_symbols = '[^\w ]+'
        stopwords = r'(^RT)'
        #hashtags = r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)" # hash-tags
        #at_mentions = r'(?:@[\w_]+)' # @-mentions. My decision is to leave these in the tweets and just remove the # and @
        tweet_urls = r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+' # URLs
        #patterns = re.compile('('+hashtags+'|'+at_mentions+'|'+tweet_urls+'|'+excess_symbols+')') # Putting excess_symbols in last is kind of a hack because order matters in this function so excess_symbols won't be removed until everything else is. 
        patterns = re.compile('('+tweet_urls+'|'+excess_symbols+'|'+stopwords+')') # Putting excess_symbols in last is kind of a hack because order matters in this function so excess_symbols won't be removed until everything else is. 
        
        # get rid of all the funky stuff 
        
        self.tweet_dataframe['filtered_text'] = [patterns.sub('', tweet['text']) for index, tweet in self.tweet_dataframe.iterrows()]  #clean tweet
        
        #Lemmatization
        # https://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python
        # could do a thing where I figure out if n v a beforehand and check. see ref
        tweet_lemmatizer = WNL()
        sentences = []
        for i in tweet_dataframe['filtered_text']:
            sentence = i.split()
            sentence = [tweet_lemmatizer.lemmatize(j, pos = 'v') for j in sentence]
            # sentence = [tweet_lemmatizer.lemmatize(j, pos = 'n') for j in sentence]
            sentences.append(" ".join(sentence))

        tweet_dataframe['filtered_text'] = pd.Series(sentences) 
        # convert to lower case:
        tweet_dataframe['filtered_text'] = tweet_dataframe['filtered_text'].str.lower()
        self.tweet_dataframe.to_csv('~/Documents/Git/Twitter-Mining/streaming_tweets/data/{}'.format(self.filename), sep='\t')
    
    def process_sentiment(self):
        """Analyze sentiment with Textblob library. Dataframe must be filtered before this method is called."""

        tweet_sentiment = [TextBlob(tweet['filtered_text']).sentiment for index, tweet in self.tweet_dataframe.iterrows()] 
        self.tweet_dataframe['polarity'] = [i.polarity for i in tweet_sentiment]
        
        self.tweet_dataframe['subjectivity'] = [i.subjectivity for i in tweet_sentiment]
        self.tweet_dataframe.to_csv('~/Documents/Git/Twitter-Mining/streaming_tweets/data/{}'.format(self.filename), sep='\t')

    
if __name__ == '__main__':
    # initiate parser in order to read in filename to analyze. 
    parser = get_parser()
    args = parser.parse_args()
   
    path = '/home/timor/Documents/Git/Twitter-Mining/streaming_tweets/data'
    os.chdir(path)
    tweet_dataframe = pd.read_csv(args.filename, sep='\t')

    analysis = process_tweet(tweet_dataframe, args.filename)
     
    analysis.filter_tweet()
    analysis.process_sentiment()
