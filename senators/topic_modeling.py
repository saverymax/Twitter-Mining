import argparse
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
"""

class modeling():
    """
    Class that contains topic modeling and visualization methods.
    """

    def __init__(self, path):
        """
        Initiate an instance.
        Must pass the whole dataframe, and individual columns to initiate. This is unnecessary, but to generate a legend, 
        the whole dataframe is required, and I only added the legend after the rest of the script had been written.
        """
        
        self.dataframe = pd.read_csv('{}filtered_tweets.tsv'.format(path), sep='\t')
        self.path = path

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

        modeling.display_topics(self, nmf, tfidf_feature_names)
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

        topics = modeling.display_topics(self, lda, tf_feature_names)

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
                    'data/word_frequencies_topic_{0}.png'.format(topic_n + 1)
                    )
        #plt.close()

        return(topics)


    def drop_tweets(self, probabilities):
        """
        Remove all tweets that have a low probability of being in all topics
        """

        print("Dropping tweets...")
        print("Shape of dataframe before dropping:", self.dataframe.shape)
        probabilities_df = pd.DataFrame(probabilities).copy()
        probabilities_df.where(probabilities_df >.7, inplace = True)
        probabilities_df.dropna(how='all', inplace = True)
        self.dataframe = self.dataframe.loc[probabilities_df.index].copy()

        print("Shape of dataframe after dropping:", self.dataframe.shape)

    def run_tsne(self, transform):
        """
        Run tsne
        """
        
        print("Beginning t-SNE reduction")
        tsne_data = TSNE(n_components = 2, verbose = 1, random_state = 0, angle = .99, init = 'pca').fit_transform(transform)
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
        ax.set_title('topics on twitter', fontsize = 20) 
        
        for i, color in zip(range(len(topics)), colors):
            ax.scatter(
                self.dataframe.loc[self.dataframe['labels'] == i, 'x'], 
                self.dataframe.loc[self.dataframe['labels'] == i, 'y'],
                label = topics[i],
                c = color)
        
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(loc='center left', bbox_to_anchor = (1, .5), fontsize = 20)

        fig.savefig(
                    'data/topics_{}.png'.format(n_topics),
                    bbox_inches = 'tight'
                    )

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
                [9, '#B8A038']])
                #[10, '#98D8D8']])
                
                #[11, '#A8B820'],
                #[12, '#7038F8'],
                #[13, '#705898'],
                #[14, '#705848'],
                #[15, '#B8B8D0'],
                #[16, '#A8A878'],
                #[17, '#EE99AC']])
        
        df_palette.columns = ['labels', 'typecolor']
        self.dataframe.merge(df_palette, on = 'labels')
        
        #Divide up the tsne data

        plot_list = []
        
        for idx, (label, color) in df_palette.iterrows():

            df_filter = self.dataframe[self.dataframe['labels'] == label]
	    
            df_filter['custom_text'] = df_filter[['username', 'text']].apply(lambda x: '<br />'.join(x), axis=1) 

            scatter = dict(
                mode = "markers",
                name = "{}".format(topics[label]), # returns label
                type = "scatter",
                text =  df_filter['custom_text'],
                showlegend = True,
                #legendgroup = "stuff", # can use this to group things in the legend
                x =  df_filter['x'], 
                y =  df_filter['y'],
                hoverinfo = 'text',
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
        offline_plot.plot(fig, filename='data/topic_model.html'.format(self.path), auto_open = False)

    def save_dataframe(self): 
        """
        Save the dataframe
        """

        print("Saving...")
        self.dataframe.to_csv('{}topic_labels_tweets.tsv'.format(self.path), sep='\t', index = False)
