#!/usr/bin/env python3
import numpy as np
import re
import string
import pandas as pd
import os
import nltk
from nltk.stem import WordNetLemmatizer as WNL
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk import pos_tag

"""
Process tsv containing tweets. 
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

    def __init__(self, path):
        """initiate instance of tweet text to be analyzed""" 

        tweet_dataframe = pd.read_csv('{}converted_tweets.tsv'.format(path), sep='\t', engine = 'python')

        self.path = path 
        self.tweet_dataframe = tweet_dataframe

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
        excess_words = r'(rt|amp)' 

        #hashtags = r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)"
        #at_mentions = r'(?:@[\w_]+)' 
        tweet_urls = r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+' # URLs
        #patterns = re.compile('('+hashtags+'|'+at_mentions+'|'+tweet_urls+'|'+excess_symbols+')') # Putting excess_symbols in last is kind of a hack because order matters in this function so excess_symbols won't be removed until everything else is. 

        patterns = re.compile('('+non_ascii+'|'+tweet_urls+'|'+excess_symbols+'|'+digits+'|'+excess_words+')') # Putting excess_symbols in last is kind of a hack because order matters in this function so excess_symbols won't be removed until everything else is. 
        
        # List comprehension way to clean tweet 
        self.tweet_dataframe['filtered_text'] = [patterns.sub('', tweet['filtered_text']) for index, tweet in self.tweet_dataframe.iterrows()]  #clean tweet
        
        # And replace all the now blank spaces with np.nan
        self.tweet_dataframe['filtered_text'] = self.tweet_dataframe['filtered_text'].replace(r'^\s*$', np.nan, regex = True)
        
        # Now remove those np.nans
        #print(self.tweet_dataframe['filtered_text'].isnull().sum())
        self.tweet_dataframe = self.tweet_dataframe.dropna()

    def lemmatization(self):
        """
        Lemmatize all tweets. This invlolves all parts of speech.
        """
        # https://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python
        # could do a thing where I figure out if n v a beforehand and check. see ref
        print("Beginning lemmatization")
        wnl = WNL()
        new_tweets = []

        for tweet in self.tweet_dataframe['filtered_text']:

            try: 
                tokenized_sentence = word_tokenize(tweet)
                pos_tag_sentence = pos_tag(tokenized_sentence)

                new_sentence = []

                for i in pos_tag_sentence:
                    tag = self.get_wordnet_pos(i[1])

                    # words like to and and don't need to be lemmatized and return ""
                    if tag != "":
                        word = wnl.lemmatize(i[0], tag)
                        new_sentence.append(word)
                    # and to, and, and other words
                    else:
                        new_sentence.append(i[0])
                
                new_sentence = " ".join(new_sentence)
                new_tweets.append(new_sentence)

            except Exception as e:
                print("Error: {0}".format(e))
        
        self.tweet_dataframe['filtered_text'] = pd.Series(new_tweets)
        self.tweet_dataframe = self.tweet_dataframe.dropna()

    def get_wordnet_pos(self, treebank_tag):
        """Get the pos tag in wordnet version"""

        # pos_tag uses treebank corpus
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            return ''

    def save_dataframe(self): 
        """
        Save the dataframe
        """

        print("Saving...")
        self.tweet_dataframe.to_csv('{}filtered_tweets.tsv'.format(self.path), sep='\t', index = False)
        #self.tweet_dataframe.to_csv('test_5.tsv', sep = '\t', index = False)

if __name__ == '__main__':
    # initiate parser in order to read in filename to analyze. 
    parser = get_parser()
    args = parser.parse_args()
   
    path = '/home/timor/Documents/Git/Twitter-Mining/streaming_tweets/data'
    os.chdir(path)

    tweet_dataframe = pd.read_csv(args.filename, sep='\t')

    process_tweet(path) 
