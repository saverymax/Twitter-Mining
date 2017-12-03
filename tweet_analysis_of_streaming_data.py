import tweepy
import sys
import json
import re
import operator
from collections import Counter
from nltk.corpus import stopwords
import string
import os
import matplotlib.pyplot as plt
import numpy as np

"""This file will read the json file stream_"the searched twitter terms".jsonl  as created by twitter_stream.py

A plot of most common terms will be generated.
"""

def tokenize(tweet):
    return tokens_re.findall(tweet)

def preprocess(tweet, lowercase = False):
    tokens = tokenize(tweet)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

def read_tweets():

    path = '/home/timor/Documents/Git/Twitter-Mining/twitter_data'
    os.chdir(path)

    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ['RT','via','amp', '...']
    
    terms_in_tweets = []

    with open('twitter_data.jsonl','r') as infile: 
        for line in infile:
            tweet = json.loads(line)
            terms_in_tweets.append(preprocess(tweet['text']))

    terms_in_tweets = sum(terms_in_tweets, [])
    
    for term in terms_in_tweets:
        if not term.startswith('#'):
            print('F')

    tweet_content = [term for term in terms_in_tweets
                    if term not in stop and not term.startswith(('#', '@'))]
   
    hashtags = [term for term in terms_in_tweets if term.startswith('#')]
    
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
    plt.xlabel('Terms used')
    plt.ylabel('Frequency of terms')
    plt.title('Term usage of Twitter Users')
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
