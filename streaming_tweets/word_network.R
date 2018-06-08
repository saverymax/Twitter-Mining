library(dplyr)
library(tidyr)
library(widyr)
library(tidytext)
library(ggplot2)
library(igraph)
library(ggraph)

# Plot coocuring words. Remember to save labels to dataframe in .py script.

# Small dataset:
#tweet_dataframe = read.csv("~/Documents/Git/Twitter-Mining/streaming_tweets/data/guns_tsne_labels.tsv", sep = '\t', stringsAsFactors = FALSE)

# Large dataset
#tweet_dataframe = read.csv("~/Documents/Git/Twitter-Mining/streaming_tweets/data/cohen_fbi_raid_tsne.tsv", sep = '\t', stringsAsFactors = FALSE)

# Liberal dataset:
#tweet_dataframe = read.csv("~/Documents/Git/Twitter-Mining/streaming_tweets/data/streaming_liberal_converted_tweets.tsv", sep = '\t', stringsAsFactors = FALSE)

# trump dataset:
tweet_dataframe = read.csv("~/Documents/Git/Twitter-Mining/trump/data/topic_labels_sentiment_converted_tweets.tsv", sep = '\t', stringsAsFactors = FALSE)


# make tibble dataframe:
# Can do per topic or for whole data set

# For a single topic:
topic = 9
tweet_dataframe_reduced <- tweet_dataframe[tweet_dataframe$labels == topic, ] 

# Coocuring words per tweet:
text = data_frame(tweet = tweet_dataframe_reduced$filtered_text, id =  tweet_dataframe_reduced$filtered_text)

# Else use tweet_dataframe for word network of full dataset
text = data_frame(tweet = tweet_dataframe$filtered_text, id =  tweet_dataframe$filtered_text)

# Can also do per topic. Don't do this with a big dataset. 
text = data_frame(tweet = tweet_dataframe$filtered_text, id =  tweet_dataframe$labels)


# Tokenize and remove stopwords
text <- text %>%
  unnest_tokens(word, tweet) %>%
  anti_join(stop_words)

text %>% count(word, sort = TRUE)

# What words occur frequently together?
word_pairs <- text %>%
  pairwise_count(word, id, sort = TRUE, upper = FALSE)

word_pairs
cutoff = 4

set.seed(1)
# If looking at specific topics:
plotFileName <- paste("~/Documents/Git/Twitter-Mining/trump/data/topic_",topic ,".png",sep="")

# if whole dataset:
#plotFileName <- paste("~/Documents/Git/Twitter-Mining/trump/data/word_network_",cutoff,".png",sep="")

png(filename = plotFileName)

word_pairs %>% 
  filter(n >= cutoff) %>%
  graph_from_data_frame() %>%
  
  ggraph(layout = "fr") +
  geom_edge_link(aes(edge_alpha = n, edge_width = n), edge_colour = "cyan4") +
  geom_node_point(size = 7) +
  geom_node_text(aes(label = name), repel = TRUE, 
                 point.padding = unit(0.2, "lines")) +
  theme_void() 

dev.off()  


