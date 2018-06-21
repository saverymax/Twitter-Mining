import argparse
import pickle
import os
import plotly_credentials
import numpy as np
import pandas as pd
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import plotly.offline as offline_plot
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation 

"""
This script perfoms LDA of NMF on a tsv of tweet data. The tweets are clustered by topic and visualized with tSNE. References and tutorials used to write
the script can be found at the bottom. 
Here is a sample call from command line:
python topic_modeling.py --path ~/Documents/Git/Twitter-Mining/streaming_tweets/data/streaming_guns_rights_guncontrol_converted_tweets.tsv

The script needs to be rewritten, using topic_modeling.ipynb for ideas. But also, it might be better to do the topic modeling in an ipynb because it's kind of an interactive exploration, and less a pipeline thing. Still thinking about it though. 
"""


def get_parser():
    """
    Set up command line options. The filename of the jsonl to be read must be given. Include file extension in the path given in the command line. 
    Documentation: 
    docs.python.org/2/library/argparse.html 
    """

    parser = argparse.ArgumentParser(description = "Modeling topics from twitter stream data") 
    parser.add_argument("--path", 
                        dest = "filename", 
                        help = "The path to the file to be analyzed. Something like /home/timor/Documents/Git/Twitter-Mining/streaming_tweets/data/tweets_converted.tsv")

    parser.add_argument("--dir", 
                        dest = "stream_dir", 
                        help = "The directory to save the figures.")
    
    parser.add_argument("--topics", 
                        dest = "n_topics", 
                        help = "The number of topics to use in the model.",
                        type = int)

    return parser


class topic_modeling():
    """
    Class that contains topic modeling and visualization methods.
    """

    def __init__(self, dataframe, filename, stream_dir):
        """
        Initiate an instance.
        Must pass the whole dataframe, and individual columns to initiate. This is unnecessary, but to generate a legend, 
        the whole dataframe is required, and I only added the legend after the rest of the script had been written.
        """

        self.dataframe = dataframe
        self.filename = filename
        self.stream_info = topic_modeling.split_filename(self)
        self.stream_dir = stream_dir

    def nmf_analysis(self, n_topics):
        """
        Vectorize and transform tweet data using the NMF algorithm, which takes a tfidf matrix as input. 
        Basic tutorial below:
        http://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html
        """
        
        n_features = 1000 

        tfidf_vectorizer = TfidfVectorizer(max_df = 0.95, min_df = 2, max_features=n_features, stop_words='english')
        # http://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
        # term frequency * inverse document frequency
        tfidf = tfidf_vectorizer.fit_transform(self.dataframe['filtered_text'])
        tfidf_feature_names = tfidf_vectorizer.get_feature_names()
        nmf = NMF(n_components = n_topics, random_state = 0, alpha= .1, l1_ratio = .5).fit(tfidf)
        nmf_transform = nmf.transform(tfidf)

        topic_modeling.display_topics(self, nmf, tfidf_feature_names)
        nmf_keys = []

        for i in range(nmf_transform.shape[0]):
            nmf_keys.append(nmf_transform[i].argmax())

        self.dataframe['labels'] = pd.Series(nmf_keys)

        return nmf_transform, topics 

    def lda_analysis(self, n_topics):
        """ 
        Vectorize and transform tweet data using LDA. LDA can only use raw term counts for LDA because it is a probabilistic graphical model,
        and hence CountVectorizer is used. 
        """

        print("Beginning LDA")
        n_features = 1000 

	# change TfidfVectorize for LDA
        tf_vectorizer = CountVectorizer(max_df = 0.95, min_df = 2, max_features = n_features, stop_words='english')
        tf = tf_vectorizer.fit_transform(self.dataframe['filtered_text'])
        tf_feature_names = tf_vectorizer.get_feature_names()
       
        lda = LatentDirichletAllocation(n_components = n_topics, max_iter = 5, learning_method = 'online', learning_offset = 50, random_state = 0).fit(tf)
        lda_transform = lda.transform(tf) 
        lda_keys = []
        for i in range(lda_transform.shape[0]):
            lda_keys.append(lda_transform[i].argmax())

        self.dataframe['labels'] = pd.Series(lda_keys)

        topics = topic_modeling.display_topics(self, lda, tf_feature_names)

        return lda_transform, topics


    def display_topics(self, model, feature_names):
        """
        Display the most frequent words per topic
        """

        n_top_words = 5 
        topics = []

        fig = plt.figure(figsize = (30, 20))

        for topic_n, topic in enumerate(model.components_):
            print("{} topics:".format(topic_n))
            frequency = list(topic.argsort()[:-n_top_words - 1:-1])
            topic_list = [feature_names[i] for i in frequency]
            topic_string = ",".join(topic_list)
            print(topic_string, "\n")
            topics.append(topic_string)

            ax = fig.add_subplot(4, 5, topic_n+1)
            index = np.arange(len(frequency))
            width = .9
            ax.bar(index, frequency, width, align = 'center')
            ax.set_xticks(index)
            font = {'fontsize': 13}
            ax.set_xticklabels(topic_list, fontdict = font, rotation = 55)
            ax.set_title('Topic {}'.format(topic_n))

        plt.tight_layout(w_pad=.2, h_pad=1)
        #plt.show()

        fig.savefig(
                    '/home/timor/Documents/Git/Twitter-Mining/streaming_tweets/data/{0}/model_word_frequencies_topic_{1}.png'.format(self.stream_dir, topic_n + 1)
                    )
        plt.close()
        
        with open("topics.pickle", 'wb') as f:
            pickle.dump(topics, f)

        return(topics)


    def drop_tweets(self, probabilities):
        """
        Remove all tweets that have a low probability of being in all topics
        """

        print("Dropping tweets...")
        print("Dimensions before dropping:", self.dataframe.shape)
        probabilities_df = pd.DataFrame(probabilities).copy()
        probabilities_df.where(probabilities_df > .8, inplace = True)
        probabilities_df.dropna(how='all', inplace = True)
        self.dataframe = self.dataframe.loc[probabilities_df.index].copy()
        print("Dimensions after dropping:", self.dataframe.shape, "\n")
        self.dataframe.reset_index(drop = True, inplace = True)

        #self.dataframe.to_csv('data/reduced_dataframe_fbi.tsv', sep='\t', index = False)
        return probabilities_df.index

    def run_tsne(self, transform):
        """
        Run tsne
        """
        
        print("Beginning t-SNE reduction")
        tsne_data = TSNE(n_components = 2, perplexity = 30, random_state = 0, init = 'pca').fit_transform(transform)
        self.dataframe['x'] = pd.Series(tsne_data[:, 0])
        self.dataframe['y'] = pd.Series(tsne_data[:, 1])

    def split_filename(self): 
        """
        Split the path given into a usable string for titles of figures and such
        """

        drive, path = os.path.splitdrive(self.filename)
        path, filename = os.path.split(path)
        filename = filename.split('.')[0]

        return filename


    def visualize_mpl(self, n_topics, topics): 
        """
        Visualize dimensionally reduced data. A matplotlib plot is produced, as well as a interactive plotly plot with, after quite a hassle, a legend. 
        """

        print("Plotting with matplotlib...")

        colors = plt.cm.nipy_spectral(np.linspace(0, 1, len(set(pd.Series(self.dataframe['labels'])))))

        fig, ax = plt.subplots(figsize = (20, 10))
        ax.set_title('{0} topics, {1}'.format(n_topics, self.stream_info), fontsize = 20) 
        
        for i, color in zip(range(len(topics)), colors):
            ax.scatter(
                self.dataframe.loc[self.dataframe['labels'] == i, 'x'], 
                self.dataframe.loc[self.dataframe['labels'] == i, 'y'],
                label = topics[i],
                c = color)
        
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor = (1, .5), fontsize = 20)


        #plt.show()
        fig.savefig(
                    #'{0}/{1}/{2}_topics_{3}.png'.format(self.filename, self.stream_dir, self.stream_info, n_topics))
                    'data/{0}/{1}_topics_{2}.png'.format(self.stream_dir, self.stream_info, n_topics), 
                    bbox_inches = 'tight'
                    )

        plt.close()


    def visualize_plotly(self, n_topics, topics):
        
        #py.sign_in(plotly_credentials.username,plotly_credentials.plotly_password)

        # Plotly with legend:
        # From https://github.com/minimaxir/pokemon-3d/blob/master/pokemon_3d_plotly.ipynb
        df_palette = pd.DataFrame([
                [0, '#C03028'],
                [1, '#F08030'],
                [2, '#6890F0'],
                [3, '#78C850'],
                [4, '#A890F0'],
                [5, '#A040A0'],
                [6, '#F8D030'],
                [7, '#E0C068'],
                [8, '#F85888'],
                [9, '#B8A038'],
                [10, '#98D8D8'],
                [11, '#A8B820'],
                [12, '#7038F8'],
                [13, '#705898'],
                [14, '#705848']])
                #[15, '#B8B8D0'],
                #[16, '#A8A878'],
                #[17, '#EE99AC']])
        
        df_palette.columns = ['labels', 'typecolor']
        self.dataframe.merge(df_palette, on = 'labels')
        
        #Divide up the tsne data

        plot_list = []
        
        for idx, (label, color) in df_palette.iterrows():

            df_filter = self.dataframe[self.dataframe['labels'] == label]
	    
            scatter = dict(
                mode = "markers",
                name = "{}".format(topics[label]), # returns label
                type = "scatter",
                text =  df_filter['text'],
                showlegend = True,
                #legendgroup = "stuff", # can use this to group things in the legend
                x =  df_filter['x'], y =  df_filter['y'],
                marker = dict(color=color))
	
            plot_list.append(scatter) 

        # Override plotly 
        empty_axis = dict(zeroline=False, showaxeslabels=False, showticklabels=False, title='')
        layout = dict(
                scene = dict(
                        xaxis = empty_axis,
                        yaxis = empty_axis,
                        ),
                    hovermode = "closest",
                    showlegend = True)

        fig = dict(data=plot_list, layout=layout)
        #plot_url = py.plot(fig)
        offline_plot.plot(fig, filename='data/{0}/{1}_topic_model_reduced.html'.format(self.stream_dir, n_topics), auto_open = True)

        #'/home/timor/Documents/Git/Twitter-Mining/streaming_tweets/data/{0}/{1}_topics_{2}.png'.format(self.stream_dir, self.stream_info, n_topics)
    def save_dataframe(self, filename): 
        """
        Save the dataframe
        """

        print("Saving...")
        
        self.dataframe.to_csv('data/cohen_reduced_dataframe_withtsne.tsv', sep='\t', index = False)
        #self.dataframe.to_csv('{}'.format(filename), sep='\t', index = False)


if __name__ == '__main__':
    # initiate parser 
    parser = get_parser()
    args = parser.parse_args()
    
    tweet_dataframe = pd.read_csv(args.filename, sep = '\t')

    # Perform analysis with NMF or LDA. Would be nice to choose from command line.
    n_topics = args.n_topics 

    model = topic_modeling(tweet_dataframe, args.filename, args.stream_dir)
    transformed_data_lda, topics = model.lda_analysis(n_topics)
	
    # If I want to plot model with only tweets most likely to be in a topic:
    reduced_index = model.drop_tweets(transformed_data_lda) 

    model.run_tsne(transformed_data_lda[reduced_index]) 

    # NMF. Not working with dropped tweets yet
    #transformed_data_nmf, topics = model.nmf_analysis(n_topics)
    #model.run_tsne(transformed_data_nmf) 
    
    # Only run if saving tsne data is necessary 
    model.save_dataframe(args.filename)

    # Visualization
    model.visualize_mpl(n_topics, topics)
    model.visualize_plotly(n_topics, topics)
