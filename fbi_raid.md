For an hour during the evening of the FBI raid of Michael Cohen's office, I streamed some tweets. I collected any tweets including the word Trump, guns, nda, Cohen, Stormy, or FBI.

More or less, this is what people were talking about

The most commonly used words. 
![Most common words on twitter during FBI raid on Michael Cohen's office](/figures/streaming/fbi_raid_terms.png)

And the most common hashtags
![Most common hashtags on twitter during FBI raid on Michael Cohen's office](/figures/streaming/fbi_raid_hashtags.png)

Word network of words used together at least 100 times
![Most common coocuring words on twitter during FBI raid](/figures/streaming/word_network_100.png)

And to thin out the network a little, word network of words used together at least 200 times
![Most common coocuring words on twitter during FBI raid](/figures/streaming/word_network_200.png)

To see what the tweets were actually about, I ran a topic model, using LDA. The words in the legend are those that best represent the topics. LDA is probabilistic, and I have included only tweets that have have a greater than 80 % chance of being in the assigned topic. Move your plot over each point to see the tweet it represents.  
[See the plot here](https://saverymax.github.io/Twitter-Mining/figures/streaming/20_topic_model_reduced)

It's interesting to see the topics, but it's more interesting to see the word networks for each topic. 

![Most common coocuring words on twitter during FBI raid](/figures/streaming/topic_0.png)
![Most common coocuring words on twitter during FBI raid](/figures/streaming/topic_8.png)
![Most common coocuring words on twitter during FBI raid](/figures/streaming/topic_14.png)
![Most common coocuring words on twitter during FBI raid](/figures/streaming/topic_17.png)
![Most common coocuring words on twitter during FBI raid](/figures/streaming/topic_18.png)
