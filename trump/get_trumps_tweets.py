import tweepy
from tweepy import OAuthHandler
import json
import sys
import os
import config
"""
This program generates a jsonl file that contains the specificed number of
tweets from trump.

To properly run the script, enter python get_trumps_tweets and the number of tweets to grab e.g., POTUS or @POTUS 200.

This file is called by get_tweets.sh. However, it can also be run independently in the command line.
"""

auth = OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_secret)

api = tweepy.API(auth)
# Download users tweets

def users_tweets(user,quantity):
    
    path = '/home/timor/Documents/Git/Twitter-Mining/trump/trumps_tweets' # Path has to be complete
    os.chdir(path)
    

    # Save a file as .jsonl that will be processed later. 'a' will add to file, w+ will writ over existing file, if I want to update. 
    with open('trumps_tweets.jsonl', 'w') as outfile: 
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
