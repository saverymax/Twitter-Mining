#!/usr/bin/env python3
import numpy as np
from textblob import TextBlob
import argparse
import re
import string
import pandas as pd
import os
import nltk
from nltk.stem import WordNetLemmatizer as WNL

"""
Process tsv containing tweets. Perform sentiment analysis on data.
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

        print("Beginning filtering")    

        # First things first convert to lowercase
        self.tweet_dataframe['filtered_text'] = self.tweet_dataframe.loc[:, 'text'].str.lower()

        # Generate all the things I want to strip away
        non_ascii = r'[^\x00-\x7F]+'
        excess_symbols = '[^\w ]+'
        digits = r'\d+'
        #stopwords = r'(rt|trump|fbi|raid|mueller|nda|cohen|corruption|corrupt|stormy|amp)'
        stopwords = r'(rt|liberal|amp)' 
        #hashtags = r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)"
        #at_mentions = r'(?:@[\w_]+)' 
        tweet_urls = r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+' # URLs
        #patterns = re.compile('('+hashtags+'|'+at_mentions+'|'+tweet_urls+'|'+excess_symbols+')') # Putting excess_symbols in last is kind of a hack because order matters in this function so excess_symbols won't be removed until everything else is. 

        patterns = re.compile('('+non_ascii+'|'+tweet_urls+'|'+excess_symbols+'|'+digits+'|'+stopwords+')') # Putting excess_symbols in last is kind of a hack because order matters in this function so excess_symbols won't be removed until everything else is. 
        
        # List comprehension way to clean tweet 
        self.tweet_dataframe['filtered_text'] = [patterns.sub('', tweet['filtered_text']) for index, tweet in self.tweet_dataframe.iterrows()]  #clean tweet
        
        # And replace all the now blank spaces with np.nan
        self.tweet_dataframe['filtered_text'] = self.tweet_dataframe['filtered_text'].replace(r'^\s*$', np.nan, regex = True)
        
        # Now remove those np.nans
        #print(self.tweet_dataframe['filtered_text'].isnull().sum())
        self.tweet_dataframe = self.tweet_dataframe.dropna()
        self.tweet_dataframe.reset_index(drop = False, inplace = True)
        # Remove all non-english words...
        # Gets rid of too much though I think 
        #words = set(nltk.corpus.words.words())
        #sentences = []
        #for tweet in self.tweet_dataframe['filtered_text']:
        #    sentence = " ".join(w for w in nltk.wordpunct_tokenize(tweet) if w in words) #or not w.isalpha())
        #    sentences.append(sentence)
    
        #self.tweet_dataframe.loc[:, 'filtered_text'] = pd.Series(sentences) 
    def lemmatization(self):
        """
        Lemmatize all tweets. This invlolves stemming nouns and verbs.
        """
        # https://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python
        # could do a thing where I figure out if n v a beforehand and check. see ref
        print("Beginning lemmatization")
        tweet_lemmatizer = WNL()
        sentences = []
        line = 0
        for i in self.tweet_dataframe['filtered_text']:
            try: 
                sentence = i.split()
                sentence = [tweet_lemmatizer.lemmatize(j, pos = 'v') for j in sentence]
                #sentence = [tweet_lemmatizer.lemmatize(j, pos = 'n') for j in sentence]
                sentences.append(" ".join(sentence))

            except Exception as e:
                print("Error: {0}, line: {1}".format(e, line))
            line += 1

        self.tweet_dataframe['filtered_text'] = pd.Series(sentences) 
        # Drop any tweets that are blank after cleaning
        self.tweet_dataframe.dropna(inplace = True)
        print(self.tweet_dataframe.isnull().sum())
    
    def process_sentiment(self):
        """Analyze sentiment with Textblob library. Dataframe must be filtered before this method is called."""

        print("Beginning sentiment analysis")
        tweet_sentiment = [TextBlob(tweet['filtered_text']).sentiment for index, tweet in self.tweet_dataframe.iterrows()] 
        self.tweet_dataframe['polarity'] = [i.polarity for i in tweet_sentiment]
        
        self.tweet_dataframe['subjectivity'] = [i.subjectivity for i in tweet_sentiment]

    def save_dataframe(self): 
        """
        Save the dataframe
        """

        print("Saving...")
        self.tweet_dataframe.to_csv('~/Documents/Git/Twitter-Mining/trump/data/sentiment_{}'.format(self.filename), sep='\t', index = False)
        #self.tweet_dataframe.to_csv('test_5.tsv', sep = '\t', index = False)


if __name__ == '__main__':
    # initiate parser in order to read in filename to analyze. 
    parser = get_parser()
    args = parser.parse_args()
   
    path = '/home/timor/Documents/Git/Twitter-Mining/trump/data'
    os.chdir(path)

    tweet_dataframe = pd.read_csv(args.filename, sep='\t')

    # fix for reading large tsv: https://github.com/pandas-dev/pandas/issues/11166
    
    # to diagnose issue:
    #import csv
    #
    #with open(args.filename, "r") as infile:
    #    read = csv.reader(infile)
    #    linenumber = 1
    #    try: 
    #        for row in read:
    #            linenumber += 1
    #    except Exception as e:
    #        print("Error is at line {0}: {1}".format(linenumber, e))
    #print(tweet_dataframe.isnull().sum())
    analysis = process_tweet(tweet_dataframe, args.filename)
    analysis.filter_tweet()
    analysis.process_sentiment()
    analysis.save_dataframe() 
