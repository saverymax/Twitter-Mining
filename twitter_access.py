import tweepy
import json
from nltk.tokenize import word_tokenize
import re
import operator
from collections import Counter
from nltk.corpus import stopwords
import string
import os
import vincent
from vincent.axes import AxisProperties
from vincent.properties import PropertySet
from vincent.values import ValueRef

"""
This file will read a json file that contains twitter data from a specific
user. In order to successfully visualize, first run this script. Then,
make sure chart.html exists in the same directory as this file. After
Next, in the directory where this file is located,
Finally, go to the address http:doubleforwardslash/localhost:8888/chart.html
"""
print(os.getcwd())
os.chdir('C:/Users/Timor/Documents/Python Scripts/twitter mining/')

def tokenize(s):
    # Tokenize tweets. Code taken from https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

# Break each tweet down into "tokens", i.e., words, symbols, or bits of meaning,
#but not sure as to # exactly what preprocess does...
def read_tweets():
    with open('user_data.json', 'r') as infile:
        text = []
        # Load the entire file at once, as opposed to one line at a time
        tweet = json.load(infile) # json.load loads a file. json.loads loads as a python dictionary
        # Generate array with all tokens of all collected tweets
        # json.dumps(text[1])) will return 1 tweet
        punctuation = list(string.punctuation)
        stop = stopwords.words('english') + punctuation + ['RT', 'via']

        #regex to remove unicode

        text = [preprocess(tweet[term]['text']) for term in range(len(tweet))]
        # Turn into one list:
        text = sum(text, [])
        # for term in text: figurin out unicode...
        #     print(re.sub(r'[^\x00-\x7F]+’,”,term))

        # Remove all the pesky symbols and words
        tweet_content = [term for term in text
                        if term not in stop and
                        not term.startswith(('#', '@'))]
        # Unicode removal:
        # revised_tweet_content = []
        # for term in tweet_content:
        #     revised_tweet_content.append(term.encode('ascii', 'ignore'))
        # print(revised_tweet_content)
        hashtags = [term for term in text if term.startswith('#')]
        return(tweet_content, hashtags)

def word_frequency(tweets):
    count_all = Counter()
    # Update the counter
    count_all.update(tweets)
    # Print the first 5 most frequent words
    print(json.dumps(count_all.most_common(5))) # weird I still have to use json.dumps
    common_words = count_all.most_common(10)
    return(common_words)

def hashtag_frequency(hashtags):
    count_all = Counter()
    count_all.update(hashtags)
    print(json.dumps(count_all.most_common(5)))
    common_hash = count_all.most_common(20)
    return(common_hash)

def visualize(common_word):
    labels, freq = zip(*common_word)
    data = {'data': freq, 'x': labels}
    bar = vincent.Bar(data, iter_idx='x')
    bar.axis_titles(x='Hastags', y='Frequency')
    # Flip the x labels 90 degrees, for readability
    x_lab = AxisProperties(labels = PropertySet(angle = ValueRef(value = 90)))
    bar.axes[0].properties = x_lab
    bar.to_json('term_freq.json')

#  @-mentions, emoticons, URLs and #hash-tags are not recognised as single tokens.
#The following code will propose a pre-processing chain that will consider
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

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

tweets = read_tweets() # Tweets will be a tuple with 2 elements
# Index 1 holds the words of the tweet; list 2 holds the hashtags
common_words = word_frequency(tweets[0])
# have yet to sort out the unicode
common_hash = hashtag_frequency(tweets[1])
visualize(common_hash)

# This function will open server and the requisite url to display the graph
# Something like: https://stackoverflow.com/questions/4302027/how-to-open-a-url-in-python
# def open_server():
#     import SocketServer
#     import SimpleHTTPServer
#
#     import requests
#     import multiprocessing
#
#     # Variables
#     PORT = 8888
#     URL = 'localhost:{port}'.format(port=PORT)
#
#     # Setup simple sever
#     Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
#     httpd = SocketServer.TCPServer(("", PORT), Handler)
#     print "Serving at port", PORT
#
#     # start the server as a separate process
#     server_process = multiprocessing.Process(target=httpd.serve_forever)
#     server_process.daemon = True
#     server_process.start()
#

# class MyListener(StreamListener):
#
#     def on_data(self, data):
#         try:
#             with open('python.json', 'a') as f:
#                 f.write(data)
#                 return True
#         except BaseException as e:
#             print("Error on_data: %s" % str(e))
#         return True
#
#     def on_error(self, status):
#         print(status)
