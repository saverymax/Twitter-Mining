import pandas
# read in line by line and maybe append to csv? 
with open('/home/timor/Documents/Git/Twitter-Mining/trump/trumps_tweets/trumps_tweets.jsonl', 'r') as infile:
    #df = pandas.read_json(infile)
    #df.to_csv('~/Documents/Git/Twitter-Mining/trump/trumps_tweets/converted_tweets.csv'
    for line in infile:
        tweet = pandas.read_json(line)
        tweet.to_csv('~/Documents/Git/Twitter-Mining/trump/trumps_tweets/converted_tweets.csv')


