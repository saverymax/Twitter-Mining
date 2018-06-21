import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly_tsne
import sentiment_analysis
import time_series_plotly
import time_series_sentiment
import pickle
import congress_pipeline


with open('topics.pickle', 'rb') as f:
    topics = pickle.load(f)

# Just for testing:
topic_sentiment = sentiment_analysis.sentiment_class(path)
sentiment_series, sentiment_layout = time_series_sentiment.time_series(path)

# Get plot data and run on dash
tsne_list, tsne_layout = plotly_tsne.generate_plot(path, topics)

series_list, series_layout = time_series_plotly.time_series(path)
boxplot_list, boxplot_layout = topic_sentiment.visualize_plotly(topics)

# Initiate dash app instance
app = dash.Dash()

app.layout = html.Div(children = [
    html.H1(children = 'Congress on twitter', style={'text-align': 'center'}),
    html.Div([
        dcc.Markdown('''What is congress doing on twitter? The purpose of this site is to summarize congress's tweet activity. 
        This site takes the five most recent tweets from each member of congress. 
        Topics are generated using latent Dirichlet allocation. 
        Sentiment scores are given to each topic.  
        See the plots below!
            ''')
            ]),
    #html.Div(children = '''What is congress doing on twitter? This site takes the five most recent tweets from every member of congress. '''),
    dcc.Graph(
        id = 't-SNE of topic clusters of tweets including the word {}',
        figure = {
            'data': tsne_list,
            'layout': tsne_layout
            }),
    dcc.Graph(
        id = 'boxplots of sentiment',
        figure = {
            'data': boxplot_list,
            'layout': boxplot_layout
            }),
     dcc.Graph(
        id = 'time series of retweets',
        figure = {
            'data': series_list,
            'layout': series_layout
            }),
    dcc.Graph(
        id = 'time series of sentiment',
        figure = {
            'data': sentiment_series,
            'layout': sentiment_layout
            }),
        ])


if __name__ == "__main__":

    app.run_server()
