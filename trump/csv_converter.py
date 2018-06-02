import pandas

"""Quick and dirty jsonl > csv"""

with open('/home/timor/Documents/Git/Twitter-Mining/trump/trumps_tweets/@readDonaldTrump.jsonl', 'r') as infile:
    #df = pandas.read_json(infile)
    #df.to_csv('~/Documents/Git/Twitter-Mining/trump/trumps_tweets/converted_tweets.csv'
    for line in infile:
        tweet = pandas.read_json(line)
        tweet.to_csv('~/Documents/Git/Twitter-Mining/trump/trumps_tweets/converted_tweets.csv')


