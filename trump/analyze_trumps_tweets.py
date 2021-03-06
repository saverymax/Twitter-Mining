import tweepy
import sys
import json
import re
import pandas as pd
import operator
from collections import Counter
from nltk.corpus import stopwords
import string
import os
import matplotlib.pyplot as plt
import numpy as np
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import seaborn as sns
import plotly_credentials

"""
This file will read the json file twitter_data.jsonl as created by get_trumps_tweets.py

It is called by tweet_workflow.sh after the tweets have been aggregated. It could also be called from the command line to visualize tweets in the file trumps_tweets.jsonl.

A plot of most common terms and hashtags will be generated. Additionally, a tsv will be created with all tweets and relevant information. This tsv will be used for sentiment analysis and time series plotting.
"""

def tokenize(tweet):
    """Turn each word/symbol in the text of the tweet into a token."""

    # The .findall method is a part of the re library.
    return tokens_re.findall(tweet)

def preprocess(tweet, lowercase = False):
    tokens = tokenize(tweet)
    # Change all tokens to lowercase, unless token is an emoticon:
    tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

def read_tweets():
    """Read tweets saved in the jsonl file, preprocess the text, and save tweets in a csv and a list. These will be filtered and visualized later."""

    path = '/home/timor/Documents/Git/Twitter-Mining/trump/data'
    os.chdir(path)

        # Create an array to hold the content of the tweets.
    terms_in_tweets = []
    tweet_list = []
    tweet_date = []
    tweet_likes = []
    tweet_RT = []
    # Read and process tweets. See above functions
    with open('realDonaldTrump.jsonl','r') as infile:
        for line in infile:
            tweet = json.loads(line)
            tweet_list.append(tweet['full_text'])
            tweet_date.append(tweet['created_at'])
            tweet_RT.append(tweet['retweet_count'])
            tweet_likes.append(tweet['favorite_count'])
            processed_tweet = preprocess(tweet['full_text'])
            terms_in_tweets.append(processed_tweet)

     # Concatenate everything into one array, for filtering and basic visualization
    terms_in_tweets = sum(terms_in_tweets, [])

    # Create dataframe to be used for time series and sentiment analysis
    tweet_dataframe = pd.DataFrame({'text': tweet_list, 'retweets': tweet_RT, 'likes': tweet_likes, 'date': tweet_date})
    #tweet_dataframe.to_csv('~/Documents/Git/Twitter-Mining/trump/data/converted_tweets.tsv',sep='\t')

    return(terms_in_tweets)

def process_tweets(terms_in_tweets):
    """Remove the text, tokens and symbols that interfere with analysis."""

    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ['rt','via','amp','h']

    tweet_content = [term for term in terms_in_tweets
                    if term not in stop and not term.startswith(('#', '@'))]

    hashtags = [term for term in terms_in_tweets if term.startswith('#')]

    # remove all non-alphanumeric content from the words:
    tweet_content = [text for text in tweet_content if not excess_symbols.search(text)]

    return(tweet_content, hashtags)

class visualize():
    """Initiate instance of twitter data."""

    def __init__(self, terms, name):
        """Initiate the instance"""

        self.terms = terms
        self.name = name

    def word_frequency(self):
        """Return the most frequent terms"""

        count_all = Counter()
        # Update the counter
        count_all.update(self.terms)
        # Print the first 5 most frequent words
        print(count_all.most_common(5))
        common_terms = count_all.most_common(20)
        return(common_terms)

    def visualize_term_usage(self):
        """Produce histogram of most frequent terms.
        Calls method word_frequency to do so.
        Could potentially be used to plot online with plotly.
        """

        #https://plot.ly/matplotlib/bar-charts/ as reference
        # Sign in to plotly
        py.sign_in(plotly_credentials.username,plotly_credentials.plotly_password)
        common_terms = self.word_frequency()
        labels, freq = zip(*common_terms)
        indexes = np.arange(len(labels))
        width = .7
        tweet_figure, axis = plt.subplots(figsize=(20, 10)) # figsize allows me to save with compatible proportions
        axis.bar(indexes, freq, width, align = 'center')
        axis.set_xticks(indexes)
        font = {'fontsize': 14}
        axis.set_xticklabels(((labels)), fontdict = font, rotation = 55)
        axis.tick_params(labelsize = 17)
        axis.set_xlabel('Terms used', fontsize = 20)
        axis.set_ylabel('Frequency of terms', fontsize = 20)
        axis.set_title('Term usage of Trump', fontsize = 22)
        tweet_figure.savefig('{0}.png'.format(self.name), bbox_inches = 'tight') # not saving correctly
        plt.show()
        plt.close()
        
        # for online plotting:
        #plotly_fig = tls.mpl_to_plotly(tweet_figure)
        #url = py.plot_mpl(tweet_figure, filename = "tweet_frequency")

# @-mentions, emoticons, URLs and #hash-tags are not recognised as single tokens.
# The following code will propose a pre-processing chain that will consider
# these aspects of the language.

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

regex_str_remove = [
    #r'[^\x00-\x7F]+' # Apparently this removes any non ascii characters.
    r'[^\w ]' # removes all non alphanumeric stuffs (except spaces). [^\w #/] will leave or other special cases
    #https://stackoverflow.com/questions/1219915/regex-to-remove-apostrophe
    ]

#if __name__ == '__main__':

#Regular expression variables
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
excess_symbols = re.compile(r'('+'|'.join(regex_str_remove)+')', re.VERBOSE | re.IGNORECASE)  # Establish regex object of symbols to be removed. Accessed in preprocess function

#Initiate data processing and visualization
tweets = read_tweets()# Lookup file
# Index 0 holds the words of the tweet; index 1 holds the dataframe.
processed_tweets = process_tweets(tweets)

common_words = visualize(processed_tweets[0], "terms")
common_words.visualize_term_usage()
common_hash = visualize(processed_tweets[1], "hashtags")
common_hash.visualize_term_usage()
