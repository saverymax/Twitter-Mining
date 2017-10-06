import tweepy
from tweepy import OAuthHandler
import json

consumer_key = '7GSXtxZvVxgMqc7zQms88Rn1A'
consumer_secret = 'DmiMJPPFbzPc0fTykPl97JIL4J0DeU69hfXrzPvw1vu2xAoYZL'
access_token = '564338092-dOtS6UWrFzLS3WDbA3YuqaEeYKMnCnMCA6kH3dPH'
access_secret = 'gOPv6wJ2xXwJBP4jU6vFpQ99Iyla5rZkLbGzYH29NAS5C'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


# Make into class
def process_or_store(tweet):
    with open('test_file.json', 'a') as outfile: # Save a file as .json, that will be processed later
        json.dump(tweet, outfile) # .dump dumps into file. .dumps turns dict into str data structure
        outfile.write('\n')
# The above code seems to do what I want it do in terms of formatting json, but there is no "," between dictionaries in file.

def read_tweets():

    with open('test_file.json', 'r') as infile:
        json_data = [json.loads(line) for line in infile]

        # Load the entire file at once, as opposed to one line at a time
    print(json.dumps(json_data)) # json.load loads a file. json.loads loads as string

# Below code adds new tweets to specified json file
for status in tweepy.Cursor(api.home_timeline).items(10):
    process_or_store(status._json)

tweets = read_tweets()
