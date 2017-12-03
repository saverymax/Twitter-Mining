import tweepy
import sys
import json
import re
import operator
from collections import Counter
from nltk.corpus import stopwords
# if cannot find package: import nltk
# nltk.download('stopwords')
import string
import os
import matplotlib.pyplot as plt
import numpy as np

"""
This file will read a json file, titled twitter_data.jason, that contains twitter data from a user specified in the twitter_json_file_creator.py script, tokenize and filter the tweet, and plot the word and hashtag usage.

The purpose of this file is to make testable individual json files. In the file tweet_analysis.py, large sets of json files will be run at one time. In this _1 version, only a hardcoded file, specified in line 41 is analyzed.
"""


def tokenize(tweet):
    # Tokenize tweets. Code taken from https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/
    return tokens_re.findall(tweet) # .findall() is a re method

def preprocess(tweet, lowercase=False):
    tokens = tokenize(tweet)


    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens] # a lowercasing feature for all the tokens that are not emoticons, e.g., :D doesn’t become :d
    return tokens

# Break each tweet down into "tokens", i.e., words, symbols, or bits of meaning,
#but not sure as to # exactly what preprocess does...
def read_tweets(): # add senators filer here and open it in next line

    path = '/home/timor/Documents/Git/Twitter-Mining/twitter_data'
    os.chdir(path)

    with open('twitter_data.json', 'r') as infile:
        text = []
        # Load the entire file at once, as opposed to one line at a time
        tweet = json.load(infile) # json.load loads a file. json.loads loads as a python dictionary
        # Generate array with all tokens of all collected tweets
        # json.dumps(text[1])) will return 1 tweet
        punctuation = list(string.punctuation)
        stop = stopwords.words('english') + punctuation + ['RT', 'via', 'amp']

        text = [preprocess(tweet[term]['text']) for term in range(len(tweet))] # For list of all tweets, process text in each tweet
        # Turn into one list:
        text = sum(text, [])
        # Remove all the pesky symbols and words
        tweet_content = [term for term in text
                        if term not in stop and
                        not term.startswith(('#', '@'))]
        tweet_content = [term for term in tweet_content if not excess_symbols.search(term)] # Remove stuff from terms
        hashtags = [term for term in text if term.startswith('#')]
        return(tweet_content, hashtags)

def word_frequency(tweets):
    count_all = Counter()
    # Update the counter
    count_all.update(tweets)
    # Print the first 5 most frequent words
    print(count_all.most_common(5)) # weird I still have to use json.dumps
    common_words = count_all.most_common(20)
    return(common_words)

def hashtag_frequency(hashtags):
    count_all = Counter()
    count_all.update(hashtags)
    print(json.dumps(count_all.most_common(5))) # For reference in command line
    common_hash = count_all.most_common(20)
    return(common_hash)

def visualize(common_word):
    labels, freq = zip(*common_word)
    indexes = np.arange(len(labels))
    width = 0.7
    plt.bar(indexes, freq, width)
    plt.xticks(indexes + width * 0.5, labels, rotation = 55)
    plt.show()
    plt.close()

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
    r'<[^>]+>', # HTML tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
    r'(?:(?:\d+,?)+(?:\.?\d+)?)',# numbers
    r'[^\x00-\x7F]+' # Apparently this removes any non ascii characters.
    ]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
excess_symbols = re.compile(r'('+'|'.join(regex_str_remove)+')', re.VERBOSE | re.IGNORECASE)  # Establish regex object of symbols to be removed. Accessed in preprocess function


tweets = read_tweets()# Lookup file
# Index 1 holds the words of the tweet; index 2 holds the hashtags
common_words = word_frequency(tweets[0])
common_hash = hashtag_frequency(tweets[1])
visualize(common_words)
visualize(common_hash)
