import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import argparse
import string
import config
import json 
import time

"""This file will generate a twitter stream of a term or set of terms, as given in the command line, for a given period of time, as specified in command line. http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html was used as documentation.
"""

def get_parser():
    """
    Set up command line options. In this program, time that stream will run and terms that will be searched for are used as command line options. As many terms as desired can be passed in command line. 
    Documentation: 
    docs.python.org/2/library/argparse.html 
    """

    parser = argparse.ArgumentParser(description = "Twitter stream") 
    parser.add_argument("--term", 
                        dest = "terms", 
                        nargs='+',
                        help = "Terms to search via twitter")
    parser.add_argument("--time",
                        dest = "time",
                        type = int,
                        help = "Time to stream tweets",
                        default = 5)
    return parser

class MyStreamListener(tweepy.StreamListener):
    """The class that will deal with all streaming data. Inherits from class defined by tweepy
    Documentation:
    https://github.com/tweepy/tweepy/blob/master/tweepy/streaming.py
    """

    def __init__(self, time_limit, start_time, term_list):
        """Initiate instance of tweet stream, setting timie_limit of the stream"""
        print("init") 
        self.time_limit = time_limit 
        self.start_time = start_time
        self.term_list = "_".join(term_list)
    def on_status(self, status):
        """Called when a new status arrives i.e., a new tweet that matches specified terms"""
        
        print(status.text)
        return True 
    def on_data(self, raw_data):
        """Called when raw data is received from connection."""
        
        while (time.time() - self.start_time) < self.time_limit:
            try:
                with open('/home/timor/Documents/Git/Twitter-Mining/streaming_tweets/data/filename.jsonl','a') as outfile:
                    outfile.write(json.dumps(raw_data)+"\n")
            except BaseException as e:
                print("Error in method on_data: {}".format(e))
                time.sleep(5) 
                pass
        print("done")
        return False 

if __name__== '__main__':
    parser = get_parser()
    args = parser.parse_args()
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)
    start_time = time.time()

    twitter_scraper = MyStreamListener(time_limit = args.time, start_time = start_time, term_list = args.terms) # Create the instance and set the time_limit. 
    tweet_stream = tweepy.Stream(auth = api.auth, listener = twitter_scraper)
    tweet_stream.filter(track=[",".join(args.terms)]) # Filter searches for all words in given list, and as args.terms is in a list, I have to unpack it first.
    tweet_stream.disconnect() #disconnect the stream and stop streaming
