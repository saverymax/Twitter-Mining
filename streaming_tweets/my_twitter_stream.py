import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListerner
import argparse
import string
import config
import json_lines

"""This file is my version of a twitter stream. http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html was used as documentation.
"""

def get_parser():
    # Code to set up command line options
    # Documentation: docs.python.org/2/library/argparse.html  
    parser = argparse.ArgumentParser(description = "Twitter stream") # Description 
    parser.add_argument("-t", "--term", 
                        dest = "term", 
                        help = "Term to search via twitter",
                        default = '-')

    return parser

class my_stream_listener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)


with open('twitter_stream_data.jsonl', 'w') as outfile:
    for item in thing:
        dump into jsonl

if __name__== '__main__':
    parer - get_parser()
    args = parser.parse_args()
    auth = OAUTHHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)
    listener = my_stream_listener() # Creates instance of class my_stream_listener
    my_stream = tweepy.Stream(auth)
    my_stream.filter(track=[args.term])

