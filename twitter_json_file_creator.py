import tweepy
from tweepy import OAuthHandler
import json

"""
This program will read a specified number of tweets from those twitter users
that I follow.
"""

consumer_key = '7GSXtxZvVxgMqc7zQms88Rn1A'
consumer_secret = 'DmiMJPPFbzPc0fTykPl97JIL4J0DeU69hfXrzPvw1vu2xAoYZL'
access_token = '564338092-dOtS6UWrFzLS3WDbA3YuqaEeYKMnCnMCA6kH3dPH'
access_secret = 'gOPv6wJ2xXwJBP4jU6vFpQ99Iyla5rZkLbGzYH29NAS5C'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
tweets = []

# Make into class
def process_or_store(tweet):
    # If I dump multiple json dictionaries into file, during for loop, json.loads will not work.
    # Instead, create list and use tweets.append. Then dump as json
     tweets.append(tweet)


# Below code adds new tweets to specified json file
for status in tweepy.Cursor(api.home_timeline).items(10):
        process_or_store(status._json)

with open('twitter_data.json', 'a') as outfile: # Save a file as .json, that will be processed later
    json.dump(tweets, outfile) # .dump dumps into file. .dumps turns dict into str data structure

# All THIS HINGES UPON ADDING TWEETS TO LIST. BUT IT SEEMS LIKE I SHOULD BE ABLE TO JUST ADD EM IN and
#NOT HAVE TO WORRY ABOUT DUPLICATES IN JSON...
# This matters when I read text in twitter_access.py and the multiple values problem occurs...
# probably a different diagnosis to make
