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
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go

"""This file will read the json file twitter_data.jsonl as created by get_users_tweets_jsonl.py
It is called by get_tweets.sh after the tweets of all senators have been aggregated. It could also be called from the command line to visualize the tweets of any individual users who have tweets save in the file twitter_data.jsonl.
A plot of most common terms will be generated.
"""

def tokenize(tweet):
    # The .findall method is a part of the re library. 
    return tokens_re.findall(tweet)

def preprocess(tweet, lowercase = False):
    tokens = tokenize(tweet)
    # Change all tokens to lowercase, unless token is an emoticon:
    tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens] 
    return tokens

def read_tweets():
    path = '/home/timor/Documents/Git/Twitter-Mining/trump/trumps_tweets'
    os.chdir(path)

    punctuation = list(string.punctuation)
    stop = stopwords.words('english') + punctuation + ['rt','via','amp','h']
    
    # Create an array to hold the content of the tweets.  
    terms_in_tweets = []
    # Read and process tweets. See above functions
    with open('trumps_tweets.jsonl','r') as infile: 
        for line in infile:
            tweet = json.loads(line)
            terms_in_tweets.append(preprocess(tweet['text']))
    
    # Concatenate everything into one array.
    terms_in_tweets = sum(terms_in_tweets, []) 
   
    # Sort the words used into hashtags and other content
    tweet_content = [term for term in terms_in_tweets
                    if term not in stop and not term.startswith(('#', '@'))]
    hashtags = [term for term in terms_in_tweets if term.startswith('#')]
   
    # remove all non-alphanumeric content from the words:
    tweet_content = [text for text in tweet_content if not excess_symbols.search(text)] 
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
    # https://plot.ly/matplotlib/bar-charts/ as reference
    # Sign in to plotly
    py.sign_in('savery_max', 'GZgmuV5Y6ERRSdx2wG8B')
    labels, freq = zip(*common_word)
    indexes = np.arange(len(labels))
    width = .7 
    tweet_figure, axis = plt.subplots()
    axis.bar(indexes, freq, width, align = 'center')
    axis.set_xticks(indexes) 
    axis.set_xticklabels(((labels)) , rotation = 55)
    axis.set_xlabel('Terms used')
    axis.set_ylabel('Frequency of terms')
    axis.set_title('Term usage of Twitter Users')
    plt.show() 
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
    #r'<[^>]+>', # HTML tags
    #r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
    #r'(?:(?:\d+,?)+(?:\.?\d+)?)',# numbers
    #r'[^\x00-\x7F]+' # Apparently this removes any non ascii characters.
    r'[^\w ]' # removes all non alphanumeric stuffs (except spaces). [^\w #/] will leave or other special cases
    #https://stackoverflow.com/questions/1219915/regex-to-remove-apostrophe
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
