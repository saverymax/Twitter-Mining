# What's going on with Trump and Twitter?

President Trump's most commonly used words, in his 500 most recent tweets
![Trumps most commonly used words in his 500 most recent tweets](/figures/trump_data/trump_terms.png)

And his most common hashtags
![Trumps most commonly used hashtags in his 500 most recent tweets](/figures/trump_data/trump_hashtags.png)

Well that's interesting but what words frequently coocur?
![trumps coocuring words](https://saverymax.github.io/Twitter-Mining/figures/trump_data/word_network_7.png)


And a slightly trimmed network:

![trumps coocuring words](https://saverymax.github.io/Twitter-Mining/figures/trump_data/word_network_10.png)

And what is going on over time? Here's an interactive time series documenting Trump's tweets and tweet metrics, from December 2017 to March 2018 
[here](https://saverymax.github.io/Twitter-Mining/figures/trump_data/trump_time_series)

And a time series from March 2018 through May
[here](https://saverymax.github.io/Twitter-Mining/figures/trump_data/march-may_trump_series)

To get an idea of what trump topics about, here is the t-SNE plot of an LDA topic model. Each point is a tweet. Hover your mouse over each point to read the text of the tweet. The legend shows the words that best represent each topic cluster. 

However, since this is a relatively small data set, the LDA algorithm does not do a super great job of clustering tweets, and there are definitely some tweets that do not really belong in the cluster they have been grouped in. I'll include another plot that does not include any tweets with a low probability of being in any given cluser, sometime. 
[See the plot here](https://saverymax.github.io/Twitter-Mining/figures/trump_data/topic_model_trump)

Words most representative of each topic

![topic words in trumps tweets](https://saverymax.github.io/Twitter-Mining/figures/trump_data/word_frequencies_topic_10.png)

And word networks for a few of the topics

Russia topic:

![topic_word_networks](https://saverymax.github.io/Twitter-Mining/figures/trump_data/topic_0.png)

great, today, whitehouse topic

![topic_word_networks](https://saverymax.github.io/Twitter-Mining/figures/trump_data/topic_2.png)

fake news topic

![topic_word_networks](https://saverymax.github.io/Twitter-Mining/figures/trump_data/topic_7.png)

trade and china topic:

![topic_word_networks](https://saverymax.github.io/Twitter-Mining/figures/trump_data/topic_10.png)


Change of a few interesting words over time. Compare to plot below.

![trumps word use over time](https://saverymax.github.io/Twitter-Mining/figures/trump_data/time_series_word_frequency.png)


Time series of the topics trump is tweeting about 

![trumps topics over time](https://saverymax.github.io/Twitter-Mining/figures/trump_data/time_series_topics.png)


