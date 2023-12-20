import pandas as pd
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
from textblob import TextBlob
import matplotlib.pyplot as plt
from collections import Counter
import warnings as ws
ws.filterwarnings("ignore")
from wordcloud import WordCloud
import json
import numpy as np
import html

# Load the four_chan.csv dataset
four_chan_path = 'four-chan.csv'
four_chan_df = pd.read_csv(four_chan_path)

# Define the cleaning function with advanced HTML and text cleaning
def clean_html_advanced(text):
    if not isinstance(text, str):
        return ""  # Return empty string for non-string data (like NaNs)

    # Decoding HTML entities
    text = html.unescape(text)

    # Removing HTML tags using regex
    clean_text = re.sub(r'<[^>]+>', ' ', text)  # Replace HTML tags with a space

    # Removing patterns like "&gt;&gt;60258018" (">>60258018" after decoding)
    clean_text = re.sub(r'>>\d+', ' ', clean_text)  # Replace '>>number' with a space

    # Removing URLs and special characters, keeping meaningful numbers
    clean_text = re.sub(r'http\S+', '', clean_text)  # Remove URLs
    clean_text = re.sub(r'[^A-Za-z0-9\s]+', '', clean_text)  # Keep meaningful numbers

    return clean_text.strip()

# Applying the advanced cleaning function to the four_chan dataset
four_chan_df['clean_comment'] = four_chan_df['p_comment'].apply(clean_html_advanced)

# Ensure NLTK resources are available
nltk.download('punkt')
nltk.download('stopwords')

# Set of English stopwords
stop_words = set(stopwords.words('english'))

# Function for text normalization and tokenization
def normalize_and_tokenize(text):
    # Convert text to lowercase
    text = text.lower()

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stopwords
    filtered_tokens = [word for word in tokens if word not in stop_words]

    return filtered_tokens

# Apply the normalization and tokenization function to the cleaned comments
four_chan_df['tokens'] = four_chan_df['clean_comment'].apply(normalize_and_tokenize)

# Function to analyze sentiment using TextBlob
def analyze_sentiment(text):
    # Creating a TextBlob object
    blob = TextBlob(text)

    # Getting the polarity score
    polarity = blob.sentiment.polarity

    # Categorizing sentiment based on polarity score
    if polarity > 0:
        return 'positive'
    elif polarity < 0:
        return 'negative'
    else:
        return 'neutral'
    
# Apply sentiment analysis to the normalized comments
four_chan_df['sentiment'] = four_chan_df['clean_comment'].apply(analyze_sentiment)

# Recomputing the sentiment distribution
sentiment_distribution = four_chan_df['sentiment'].value_counts()

# Plotting the sentiment distribution
plt.figure(figsize=(8, 6))
sentiment_distribution.plot(kind='bar', color=['green', 'red', 'blue'])
plt.title('Sentiment Distribution in 4chan Dataset')
plt.xlabel('Sentiment')
plt.ylabel('Number of Comments')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Defining the set of keywords for gun culture and hate speech
gun_culture_keywords = ['gun', 'firearm', 'rifle', 'shotgun', 'pistol', 'ammo', 'magazine', 
                        '2nd amendment', 'self-defense', 'concealed carry']
hate_speech_keywords = ['hate', 'attack', 'violence', 'threat', 'discrimination', 'extremist', 
                        'radical', 'offensive', 'insult', 'harassment']

# Combining the lists for analysis
all_keywords = gun_culture_keywords + hate_speech_keywords

# Function to count keyword frequencies using the tokenized data
def count_keywords(tokens, keywords):
    # Count occurrences of each keyword
    return Counter(token for token in tokens if token in keywords)

# Counting keyword frequencies in the dataset
keyword_counts = Counter()
for tokens in four_chan_df['tokens']:
    keyword_counts.update(count_keywords(tokens, all_keywords))

# Converting the counter to a dictionary for easier visualization
keyword_freq_dict = dict(keyword_counts)

# Preparing data for bar chart visualization
keyword_names = list(keyword_freq_dict.keys())
keyword_values = list(keyword_freq_dict.values())

# Plotting the keyword frequency bar chart
plt.figure(figsize=(12, 8))
plt.bar(keyword_names, keyword_values, color='skyblue')
plt.title('Keyword Frequencies in 4chan Dataset')
plt.xlabel('Keywords')
plt.ylabel('Frequency')
plt.xticks(rotation=45, ha="right")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Generating the word cloud
wordcloud = WordCloud(width=800, height=400, background_color ='white').generate_from_frequencies(keyword_freq_dict)

# Displaying the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Keyword Word Cloud in 4chan Dataset')
plt.show()

# Converting 'datetime' column to datetime format
four_chan_df['datetime'] = pd.to_datetime(four_chan_df['datetime'])
four_chan_df['year'] = four_chan_df['datetime'].dt.year

# Counting posts per year
posts_per_year = four_chan_df['year'].value_counts().sort_index()

# Filtering the dataset for the year 2023
four_chan_2023 = four_chan_df[four_chan_df['year'] == 2023]

# Extracting month and day information
four_chan_2023['month'] = four_chan_2023['datetime'].dt.month
four_chan_2023['day'] = four_chan_2023['datetime'].dt.day

# Grouping by month and day to count posts
posts_by_date_2023 = four_chan_2023.groupby(['month', 'day']).size()

# Plotting the time series of posts in 2023
plt.figure(figsize=(12, 6))
posts_by_date_2023.plot(kind='line', color='blue', marker='o')
plt.title('Time Series of Posts in 2023 (4chan Dataset)')
plt.xlabel('Month and Day')
plt.ylabel('Number of Posts')
plt.grid(True)
plt.show()

# Loading the Reddit dataset
reddit_path = 'reddit.csv'
reddit_df = pd.read_csv(reddit_path)

# Applying the cleaning function to 'title', 'self_text', and 'comments'
reddit_df['clean_title'] = reddit_df['title'].apply(clean_html_advanced)
reddit_df['clean_self_text'] = reddit_df['self_text'].apply(clean_html_advanced)

def extract_and_clean_comments(json_comments):
    try:
        comments_list = json.loads(json_comments)
        all_comments = ' '.join([clean_html_advanced(comment['comments'][0]['body']) for comment in comments_list])
        return all_comments
    except:
        return ""
    
reddit_df['clean_comments'] = reddit_df['comments'].apply(extract_and_clean_comments)

# Applying normalization and tokenization to the Reddit dataset
reddit_df['tokens_title'] = reddit_df['clean_title'].apply(normalize_and_tokenize)
reddit_df['tokens_self_text'] = reddit_df['clean_self_text'].apply(normalize_and_tokenize)
reddit_df['tokens_comments'] = reddit_df['clean_comments'].apply(normalize_and_tokenize)

# Applying sentiment analysis to the title, self_text, and comments
reddit_df['sentiment_title'] = reddit_df['clean_title'].apply(analyze_sentiment)
reddit_df['sentiment_self_text'] = reddit_df['clean_self_text'].apply(analyze_sentiment)
reddit_df['sentiment_comments'] = reddit_df['clean_comments'].apply(analyze_sentiment)

# Aggregating sentiment analysis results for title, self_text, and comments
sentiment_title_distribution = reddit_df['sentiment_title'].value_counts()
sentiment_self_text_distribution = reddit_df['sentiment_self_text'].value_counts()
sentiment_comments_distribution = reddit_df['sentiment_comments'].value_counts()

# Plotting the sentiment distribution for title, self_text, and comments
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Title Sentiment Distribution
axes[0].bar(sentiment_title_distribution.index, sentiment_title_distribution.values, color=['blue', 'green', 'red'])
axes[0].set_title('Title Sentiment Distribution')
axes[0].set_xlabel('Sentiment')
axes[0].set_ylabel('Count')
axes[0].grid(axis='y', linestyle='--', alpha=0.7)

# Self Text Sentiment Distribution
axes[1].bar(sentiment_self_text_distribution.index, sentiment_self_text_distribution.values, color=['blue', 'green', 'red'])
axes[1].set_title('Self Text Sentiment Distribution')
axes[1].set_xlabel('Sentiment')
axes[1].set_ylabel('Count')
axes[1].grid(axis='y', linestyle='--', alpha=0.7)

# Comments Sentiment Distribution
axes[2].bar(sentiment_comments_distribution.index, sentiment_comments_distribution.values, color=['blue', 'green', 'red'])
axes[2].set_title('Comments Sentiment Distribution')
axes[2].set_xlabel('Sentiment')
axes[2].set_ylabel('Count')
axes[2].grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

# Function to count keyword frequencies in tokenized lists
def count_keywords_in_list(tokens, keywords):
    return Counter(kw for kw in keywords if kw in tokens)

# Counting keyword frequencies in the Reddit dataset
reddit_keyword_counts = Counter()
for tokens in reddit_df['tokens_title']:
    reddit_keyword_counts.update(count_keywords_in_list(tokens, all_keywords))
for tokens in reddit_df['tokens_self_text']:
    reddit_keyword_counts.update(count_keywords_in_list(tokens, all_keywords))
for tokens in reddit_df['tokens_comments']:
    reddit_keyword_counts.update(count_keywords_in_list(tokens, all_keywords))

# Converting the counter to a dictionary for easier visualization
reddit_keyword_freq_dict = dict(reddit_keyword_counts)

# Preparing data for bar chart visualization
reddit_keyword_names = list(reddit_keyword_freq_dict.keys())
reddit_keyword_values = list(reddit_keyword_freq_dict.values())

# Plotting the keyword frequency bar chart for Reddit dataset
plt.figure(figsize=(12, 8))
plt.bar(reddit_keyword_names, reddit_keyword_values, color='skyblue')
plt.title('Keyword Frequencies in Reddit Dataset')
plt.xlabel('Keywords')
plt.ylabel('Frequency')
plt.xticks(rotation=45, ha="right")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Generating the word cloud for Reddit dataset
reddit_wordcloud = WordCloud(width=800, height=400, background_color ='white').generate_from_frequencies(reddit_keyword_freq_dict)

# Displaying the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(reddit_wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Keyword Word Cloud in Reddit Dataset')
plt.show()

# Creating a synthetic datetime column for Reddit dataset, focusing on 2023
# Generating random dates within 2023
np.random.seed(0)  # For reproducibility
random_dates_2023 = pd.date_range(start='2023-09-19', end='2023-12-10', freq='D')
reddit_df['datetime'] = np.random.choice(random_dates_2023, size=len(reddit_df))

# Extracting year, month, and day information
reddit_df['year'] = reddit_df['datetime'].dt.year
reddit_df['month'] = reddit_df['datetime'].dt.month
reddit_df['day'] = reddit_df['datetime'].dt.day

# Filtering the dataset for the year 2023
reddit_2023 = reddit_df[reddit_df['year'] == 2023]

# Grouping by month and day to count posts
reddit_posts_by_date_2023 = reddit_2023.groupby(['month', 'day']).size()

# Plotting the time series of posts in 2023 for Reddit dataset
plt.figure(figsize=(20, 6))
reddit_posts_by_date_2023.plot(kind='line', color='blue', marker='o')
plt.title('Synthetic Time Series of Posts in 2023 (Reddit Dataset)')
plt.xlabel('Month and Day')
plt.ylabel('Number of Posts')
plt.grid(True)
plt.show()

# Making new datasets for dashboarrd

# Preprocess 4chan Dataset
four_chan_df['clean_comment'] = four_chan_df['p_comment'].apply(clean_html_advanced)
four_chan_df['tokens'] = four_chan_df['clean_comment'].apply(normalize_and_tokenize)
four_chan_df['sentiment'] = four_chan_df['clean_comment'].apply(analyze_sentiment)
four_chan_df['datetime'] = pd.to_datetime(four_chan_df['datetime'])

# Selecting only necessary columns for 4chan
four_chan_columns = ['datetime', 'clean_comment', 'tokens', 'sentiment']
four_chan_processed = four_chan_df[four_chan_columns]

# Save the optimized 4chan data to a CSV file
four_chan_processed.to_csv('optimized_four_chan.csv', index=False)

# Preprocess Reddit Dataset
reddit_df['clean_title'] = reddit_df['title'].apply(clean_html_advanced)
reddit_df['clean_self_text'] = reddit_df['self_text'].apply(clean_html_advanced)
reddit_df['clean_comments'] = reddit_df['comments'].apply(clean_html_advanced)
reddit_df['tokens_title'] = reddit_df['clean_title'].apply(normalize_and_tokenize)
reddit_df['tokens_self_text'] = reddit_df['clean_self_text'].apply(normalize_and_tokenize)
reddit_df['tokens_comments'] = reddit_df['clean_comments'].apply(normalize_and_tokenize)
reddit_df['sentiment_title'] = reddit_df['clean_title'].apply(analyze_sentiment)
reddit_df['sentiment_self_text'] = reddit_df['clean_self_text'].apply(analyze_sentiment)
reddit_df['sentiment_comments'] = reddit_df['clean_comments'].apply(analyze_sentiment)

# Creating a synthetic datetime column for Reddit
np.random.seed(0)
random_dates_2023 = pd.date_range(start='2023-09-19', end='2023-12-31', freq='D')
reddit_df['datetime'] = np.random.choice(random_dates_2023, size=len(reddit_df))

# Selecting only necessary columns for Reddit
reddit_columns = ['datetime', 'clean_title', 'clean_self_text', 'clean_comments', 
                  'tokens_title', 'tokens_self_text', 'tokens_comments', 
                  'sentiment_title', 'sentiment_self_text', 'sentiment_comments']
reddit_processed = reddit_df[reddit_columns]

# Save the optimized Reddit data to a CSV file
reddit_processed.to_csv('optimized_reddit.csv', index=False)