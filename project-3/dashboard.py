# Importing necessary libraries
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go
import datetime
from collections import Counter
from plotly.subplots import make_subplots
import ast

# Load optimized datasets for 4Chan and Reddit platforms
four_chan_df = pd.read_csv('optimized_four_chan.csv')
reddit_df = pd.read_csv('optimized_reddit.csv')

# Function to convert string representation of lists back into lists
def convert_to_list(string):
    try:
        return ast.literal_eval(string)
    except:
        return []

# Apply conversion to dataset columns that contain tokenized data
four_chan_df['tokens'] = four_chan_df['tokens'].apply(convert_to_list)
reddit_df['tokens_self_text'] = reddit_df['tokens_self_text'].apply(convert_to_list)
reddit_df['tokens_title'] = reddit_df['tokens_title'].apply(convert_to_list)
reddit_df['tokens_comments'] = reddit_df['tokens_comments'].apply(convert_to_list)

# Defining keywords related to gun culture and hate speech for analysis
gun_culture_keywords = ['gun', 'firearm', 'rifle', 'shotgun', 'pistol', 'ammo', 'magazine', 
                        '2nd amendment', 'self-defense', 'concealed carry']
hate_speech_keywords = ['hate', 'attack', 'violence', 'threat', 'discrimination', 'extremist', 
                        'radical', 'offensive', 'insult', 'harassment']
all_keywords = gun_culture_keywords + hate_speech_keywords

# Functions to count occurrences of each keyword in tokenized data
def count_keywords(tokens, keywords):
    return Counter(token for token in tokens if token in keywords)

def count_keywords_in_list(tokens, keywords):
    return Counter(kw for kw in keywords if kw in tokens)

# Streamlit app layout and user input fields
st.title('Interactive Dashboard for Gun Culture and Hate Speech Analysis')
platform = st.selectbox('Choose a Platform:', ['4Chan', 'Reddit'])

# Setting up date range for analysis
min_date = pd.to_datetime('2023-01-01').to_pydatetime()
max_date = datetime.datetime.now()

# Initializing session state for start and end dates
if 'start_date' not in st.session_state:
    st.session_state['start_date'] = min_date
if 'end_date' not in st.session_state:
    st.session_state['end_date'] = max_date

# Create two date input fields for start and end date
start_date = st.date_input('Start Date', value=st.session_state['start_date'], min_value=min_date, max_value=max_date)
end_date = st.date_input('End Date', value=st.session_state['end_date'], min_value=min_date, max_value=max_date)

# Update session state
st.session_state['start_date'] = start_date
st.session_state['end_date'] = end_date

def display_plots(data, platform_name):
    # Nested functions for different types of plots: sentiment analysis, keyword frequency, time series, word cloud
    # Sentiment analysis plot
    def sentiment_analysis_plot():
        # Different handling for Reddit and 4Chan due to different data structures
        if platform_name == 'Reddit':
            if data.empty:
                st.write(f"No sentiment data available for {platform_name} in the selected date range.")
            else:
                sentiment_title_distribution = data['sentiment_title'].value_counts()
                sentiment_self_text_distribution = data['sentiment_self_text'].value_counts()
                sentiment_comments_distribution = data['sentiment_comments'].value_counts()

                fig = make_subplots(rows=1, cols=3, subplot_titles=("Title Sentiment", "Self Text Sentiment", "Comments Sentiment"))

                fig.add_trace(go.Bar(x=sentiment_title_distribution.index, y=sentiment_title_distribution.values), row=1, col=1)
                fig.add_trace(go.Bar(x=sentiment_self_text_distribution.index, y=sentiment_self_text_distribution.values), row=1, col=2)
                fig.add_trace(go.Bar(x=sentiment_comments_distribution.index, y=sentiment_comments_distribution.values), row=1, col=3)

                fig.update_layout(title_text='Sentiment Distributions in Reddit Dataset', showlegend=False)
                st.plotly_chart(fig)

        elif platform_name == '4Chan':
            if data.empty:
                st.write(f"No sentiment data available for {platform_name} in the selected date range.")
            else:
                sentiment_distribution = data['sentiment'].value_counts()
                fig = px.bar(sentiment_distribution, title='Sentiment Distribution in 4Chan Dataset',
                            labels={'index': 'Sentiment', 'value': 'Count'})
                st.plotly_chart(fig)

    # Keyword frequencies plot
    def keyword_frequency_plot():
        if platform_name == 'Reddit':
            reddit_keyword_counts = Counter()
            for tokens in data['tokens_title']:
                reddit_keyword_counts.update(count_keywords_in_list(tokens, all_keywords))
            for tokens in data['tokens_self_text']:
                reddit_keyword_counts.update(count_keywords_in_list(tokens, all_keywords))
            for tokens in data['tokens_comments']:
                reddit_keyword_counts.update(count_keywords_in_list(tokens, all_keywords))
            keyword_freq_dict = dict(reddit_keyword_counts)
        else:
            keyword_counts = Counter()
            for tokens in data['tokens']:
                keyword_counts.update(count_keywords(tokens, all_keywords))
            keyword_freq_dict = dict(keyword_counts)

        # Check if the keyword frequency dictionary is empty
        if not keyword_freq_dict:
            st.write(f"No data available for {platform_name} in the selected date range.")
        else:
            fig = px.bar(x=list(keyword_freq_dict.keys()), y=list(keyword_freq_dict.values()),
                        title=f'Keyword Frequencies in {platform_name} Dataset',
                        labels={'x': 'Keywords', 'y': 'Frequency'})
            st.plotly_chart(fig)

    # Time series plot
    def time_series_plot():
        if data.empty:
            st.write(f"No time series data available for {platform_name} in the selected date range.")
        else:
            time_series_data = data.groupby(pd.to_datetime(data['datetime']).dt.date).size()
            fig = px.line(time_series_data, title=f'Time Series of Posts in {platform_name} Dataset',
                        labels={'index': 'Date', 'value': 'Number of Posts'})
            st.plotly_chart(fig)

    # Word Cloud plot
    def word_cloud_plot():
        if platform_name == 'Reddit':
            reddit_keyword_counts = Counter()
            for tokens in data['tokens_title']:
                reddit_keyword_counts.update(count_keywords_in_list(tokens, all_keywords))
            for tokens in data['tokens_self_text']:
                reddit_keyword_counts.update(count_keywords_in_list(tokens, all_keywords))
            for tokens in data['tokens_comments']:
                reddit_keyword_counts.update(count_keywords_in_list(tokens, all_keywords))
            keyword_freq_dict = dict(reddit_keyword_counts)
        else:
            keyword_counts = Counter()
            for tokens in data['tokens']:
                keyword_counts.update(count_keywords(tokens, all_keywords))
            keyword_freq_dict = dict(keyword_counts)

        if not keyword_freq_dict:
            st.write(f"No data available for {platform_name} in the selected date range.")
        else:
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(keyword_freq_dict)

            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            ax.set_title(f'Word Cloud in {platform_name} Dataset')
            st.pyplot(fig)

    # Calling the plotting functions
    sentiment_analysis_plot()
    keyword_frequency_plot()
    time_series_plot()
    word_cloud_plot()

# Converting start and end dates to pandas timestamps for filtering
start_timestamp = pd.to_datetime(start_date)
end_timestamp = pd.to_datetime(end_date)

# Filtering data based on the selected platform and date range
if platform == '4Chan':
    filtered_data = four_chan_df[(pd.to_datetime(four_chan_df['datetime']) >= start_timestamp) & 
                                 (pd.to_datetime(four_chan_df['datetime']) <= end_timestamp)]
    display_plots(filtered_data, '4Chan')
else:
    filtered_data = reddit_df[(pd.to_datetime(reddit_df['datetime']) >= start_timestamp) & 
                              (pd.to_datetime(reddit_df['datetime']) <= end_timestamp)]
    display_plots(filtered_data, 'Reddit')
