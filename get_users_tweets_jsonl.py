import tweepy
from tweepy import OAuthHandler
import json
import sys
import os
"""
This program generates a json file that contains the specificed number of
tweets from a specified user, or the concatenated dictionary of tweets from multiple users (if called by get_tweets.sh).

To properly run the script, enter python user_tweet.py screen name for twitter user; number of tweets to grab e.g., POTUS or @POTUS 200

This file is called by get_tweets.sh. However, it can also be run independently in the command line. However, there is currently no way to call from the command line the user/s of interest 
"""

consumer_key = '7GSXtxZvVxgMqc7zQms88Rn1A'
consumer_secret = 'DmiMJPPFbzPc0fTykPl97JIL4J0DeU69hfXrzPvw1vu2xAoYZL'
access_token = '564338092-dOtS6UWrFzLS3WDbA3YuqaEeYKMnCnMCA6kH3dPH'
access_secret = 'gOPv6wJ2xXwJBP4jU6vFpQ99Iyla5rZkLbGzYH29NAS5C'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
# Download users tweets

def users_tweets(user,quantity):
    
    path = '/home/timor/Documents/Git/Twitter-Mining/twitter_data' # Path has to be complete
    os.chdir(path)
    

    # Save a file as .jsonl that will be processed later. 'a' will add to file, w+ will writ over existing file, if I want to update. 
    with open('twitter_data.jsonl', 'a') as outfile: 
    #make initial request for most recent tweets (200 is the maximum allowed count)
        for tweet in tweepy.Cursor(api.user_timeline, screen_name = user).items(int(quantity)):    
            outfile.write(json.dumps(tweet._json)+"\n") # This is a weird way to do this because it just prints out the json string and writes that to a file. As opposed to json.dump which will actually write to the file directly. Could also do json.dump(stuff) and then outfile.write("\n"). Not so great either.   

if __name__ == '__main__':

    #get tweets for username passed at command line. Just = Enter username when calling file
    if len(sys.argv) == 3:
        users_tweets(sys.argv[1],sys.argv[2]) # Element one is the file
    else:
        print("Error: enter one username followed by the number of tweets to grab")
# Add try except to above code

# Used https://github.com/gitlaura/get_tweets/blob/master/get_tweets.py to create script
