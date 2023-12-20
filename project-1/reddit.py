
# """Below data pushing to db"""
import time
import requests
import psycopg2
from psycopg2 import extras
import csv

# Define your Reddit API credentials
client_id = 'reddit_dev_client_id'
client_secret = 'reddit_dev_client_secret'
user_agent = 'reddit_dev_username'

# Reddit API authentication
auth = requests.auth.HTTPBasicAuth(client_id, client_secret)

# Define your PostgreSQL database connection parameters

DB_PARAMS = {
    "dbname": "db_name",            # Replace with your PostgreSQL database name
    "user": "db_user",              # Replace with your PostgreSQL username
    "password": "db_password",      # Change if your database is hosted elsewhere
    "host": "localhost",            # Change if your database is hosted elsewhere
    "port": "5432"                  # Change if your PostgreSQL port is different
}

def extract_comments(data, submission_id, headers, auth):
    url = f'https://www.reddit.com/comments/{submission_id}.json'
    response = requests.get(url, headers=headers, auth=auth)
    
    if response.status_code == 200:
        submission_data = response.json()
        submission_info = {
            'comments': []
        }
        
        for comment in submission_data[1]['data']['children']:
            comment_data = comment['data']
            # Check if 'author' key exists in the comment_data dictionary
            if 'author' in comment_data:
                author = comment_data['author']
            else:
                author = None  # or any default value you prefer
            submission_info['comments'].append({
                'author': author,
                # 'score': comment_data['score'],
                'score': comment_data.get('score', None),
                # 'body': comment_data['body']
                'body': comment_data.get('body', None)
            })
        
        data.append(submission_info)

# Define the Reddit API endpoint and parameters
base_url = 'https://www.reddit.com/r/'
subreddits = ['gun','gunsarecool', 'guns', 'firearms', 'progun','secondamendment', 'progun', 'guncontrol',
              'massshooting',]
limit = 100
data = []

conn = psycopg2.connect(**db_params)
cur = conn.cursor(cursor_factory=extras.DictCursor)

# Create a table for Reddit data
cur.execute("""
    CREATE TABLE IF NOT EXISTS reddit_data (
        title text,
        self_text text,
        author text,
        score integer,
        num_comments integer,
        upvote_ratio numeric,
        comments json
    );
""")

for subreddit_name in subreddits:
    # Initialize variables for pagination
    records_fetched = 0
    after = None
    try:
        # Continue fetching until 1000 records are obtained
        while records_fetched < 1000:
            # Retrieve subreddit data with pagination
            url = f'{base_url}{subreddit_name}/top.json?limit=100&after={after}'
            headers = {'User-Agent': user_agent}
            response = requests.get(url, headers=headers, auth=auth)
            if response.status_code == 429:  # Rate limit error
                print(f"Rate limited. Waiting for 60 seconds.")
                time.sleep(60)  # Wait for 60 seconds to avoid rate limiting
                continue  # Retry the request after the delay
            if response.status_code == 200:
                subreddit_data = response.json()
                for submission in subreddit_data['data']['children']:
                    submission_data = submission['data']

                    # Extract required information
                    submission_info = {
                        'title': submission_data['title'],
                        'self_text': submission_data['selftext'],
                        'author': submission_data['author'],
                        'score': submission_data['score'],
                        'num_comments': submission_data['num_comments'],
                        'upvote_ratio': submission_data['upvote_ratio'],
                        'comments': []
                    }

                    # Process comments (using your existing extract_comments function here if needed)

                    # Append the data to a list for bulk insert
                    cur.execute("""
                        INSERT INTO reddit_data VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;
                    """, (
                        submission_info['title'], submission_info['self_text'], submission_info['author'],
                        submission_info['score'], submission_info['num_comments'], submission_info['upvote_ratio'],
                        psycopg2.extras.Json(submission_info['comments'])
                    ))

                    # Increment the count of fetched records
                    records_fetched += 1

                # Get the 'after' value for the next page (for pagination)
                after = subreddit_data['data']['after']
                if after is None:
                    break  # No more pages to fetch
            else:
                print(f"Failed to fetch data from {subreddit_name}. Error: {response.status_code}")
                break  # Stop fetching for this subreddit due to error
    except Exception as e:
        print(f"Error occurred while fetching data from {subreddit_name}: {e}")

# Commit changes and close the database connection
conn.commit()
cur.close()
conn.close()

# Print a message to indicate that the data has been saved to the database
print("Data saved to the PostgreSQL database.")
