import plotly.plotly as py
import pickle
import plotly.tools as tls
import plotly.graph_objs as go
import plotly.offline as offline_plot
import pandas as pd

def generate_plot(path, topics):
    """
    Generate plot layout and data and dash
    """

    tweet_dataframe = pd.read_csv('{}cohen_reduced_dataframe_withtsne.tsv'.format(path), sep='\t')
       
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
            [14, '#705848'],
            [15, '#B8B8D0'],
            [16, '#A8A878'],
            [17, '#EE99AC'],
            [18, '#ABEBC6'],
            [19, '#B9770E']])

    df_palette.columns = ['labels', 'typecolor']
    tweet_dataframe.merge(df_palette, on = 'labels')

    plot_list = []

    for idx, (label, color) in df_palette.iterrows():

        df_filter = tweet_dataframe.loc[tweet_dataframe['labels'] == label].copy()
        
        #df_filter['custom_text'] = df_filter.loc[:, ['username', 'text']].apply(lambda x: '<br />'.join(x), axis=1) 

        scatter = dict(
            mode = "markers",
            name = topics[label], # add topics here 
            type = "scatter",
            text = df_filter['text'],
            #text =  df_filter['custom_text'],
            hoverinfo = 'text',
            showlegend = True,
            #legendgroup = "stuff", # can use this to group things in the legend
            x =  df_filter['x'], 
            y =  df_filter['y'],
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
    
    return plot_list, layout

    #https://dash.plot.ly/getting-started
    # i don't know what to do with this. could do topic modeling script in dash.

if __name__ == "__main__":

    path = 'data/'

    with open('topics.pickle', 'rb') as f:
        topics = pickle.load(f)

    plot_list, layout = generate_plot(path, topics)
    fig = dict(data=plot_list, layout=layout)
    #offline_plot.plot(fig, filename='data/topic_model.html', auto_open = True)

    offline_plot.plot(fig, filename='data/topic_model.html', auto_open = False)
    


