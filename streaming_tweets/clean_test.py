#!/usr/bin/env python3
import argparse
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



def filter_tweet():
    """Remove chosen elements from tweets. Depending on hardcoded values, this might be hashtags, @mentions, urls, or all non-alphanumeric characters."""

    print("Beginning filtering")    


    text = 'rt heart. lets try'

    # First things first convert to lowercase

    # Generate all the things I want to strip away
    non_ascii = r'[^\x00-\x7F]+'
    excess_symbols = '[^\w ]+'
    digits = r'\d+'
    #stopwords = r'(rt|trump|fbi|raid|mueller|nda|cohen|corruption|corrupt|stormy|amp)'
    excess_words = r'(^rt|amp)' 

    #hashtags = r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)"
    #at_mentions = r'(?:@[\w_]+)' 
    tweet_urls = r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+' # URLs
    #patterns = re.compile('('+hashtags+'|'+at_mentions+'|'+tweet_urls+'|'+excess_symbols+')') # Putting excess_symbols in last is kind of a hack because order matters in this function so excess_symbols won't be removed until everything else is. 

    patterns = re.compile('('+non_ascii+'|'+tweet_urls+'|'+excess_symbols+'|'+digits+'|'+excess_words+')') # Putting excess_symbols in last is kind of a hack because order matters in this function so excess_symbols won't be removed until everything else is. 
    
    # List comprehension way to clean tweet 
    new_text = patterns.sub('', text)  #clean tweet
    print(new_text)
    
    return new_text

def lemmatization(tweet):
    """
    Lemmatize all tweets. This invlolves all parts of speech.
    """
    # https://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python
    # could do a thing where I figure out if n v a beforehand and check. see ref
    print("Beginning lemmatization")
    wnl = WNL()

    tweet

    try: 
        tokenized_sentence = word_tokenize(tweet)
        pos_tag_sentence = pos_tag(tokenized_sentence)

        new_sentence = []

        for i in pos_tag_sentence:
            tag = get_wordnet_pos(i[1])

            # words like to and and don't need to be lemmatized and return ""
            if tag != "":
                word = wnl.lemmatize(i[0], tag)
                new_sentence.append(word)
            # and to, and, and other words
            else:
                new_sentence.append(i[0])
        
        new_sentence = " ".join(new_sentence)
        print(new_sentence,"\n")

    except Exception as e:
        print("Error: {0}".format(e))


def get_wordnet_pos(treebank_tag):
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

if __name__ == '__main__':
    # initiate parser in order to read in filename to analyze. 

    tweet = filter_tweet()
    lemmatization(tweet)
