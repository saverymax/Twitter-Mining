# To run this code, first edit config.py with your configuration, then:
#
# mkdir data
# python twitter_stream_download.py -q apple -d data
#
# It will produce the list of tweets for the query "apple"
# in the file data/stream_apple.json

import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import argparse
import string
import config
import json

def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')
    parser.add_argument("-d",
                        "--data-dir",
                        dest="data_dir",
                        help="Output/Data Directory")
    return parser


class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""

    def __init__(self, start_time, time_limit, data_dir, query):
        self.time = start_time
        self.limit = time_limit
        self.tweet_data = []
        query_fname = format_filename(query)
        self.outfile = "%s/stream_%s.json" % (data_dir, query_fname)

    def on_data(self, data):
        print("on_data function")
        while (time.time() - self.time) < self.limit:
            try:
                with open(self.outfile, 'a') as file:
                    print(type(data))
                    file.write(data)
                    #print(data)
                    return True
            except BaseException as e:
                print("Error on_data: %s" % str(e))
                time.sleep(5)
            return True

    def on_error(self, status):
        print(status)
        return True


def format_filename(fname):
    """Convert file name into a safe string.
    Arguments:
        fname -- the file name to convert
    Return:
        String -- converted file name
    """
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    """Convert a character into '_' if invalid.
    Arguments:
        one_char -- the char to convert
    Return:
        Character -- converted char
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'

@classmethod
def parse(cls, api, raw): # parse is called in on_data in tweepy docs: https://github.com/tweepy/tweepy/blob/master/tweepy/streaming.py
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    auth = OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_secret)
    api = tweepy.API(auth)
# add timer here
    start_time = time.time()
    twitter_stream = Stream(auth, MyListener(start_time, time_limit = 5, data_dir = args.data_dir, query = args.query)) # using tweepy functionality
    twitter_stream.filter(track=[args.query]) # Searches for term of interest
    twitter_stream.disconnect() #disconnect the stream and stop streaming
