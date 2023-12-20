import requests
import psycopg2
from psycopg2 import extras

fetched = []
comments_fetched = []
API_URL = "https://a.4cdn.org"

DB_PARAMS = {
    "dbname": "db_name",
    "user": "db_user",
    "password": "db_password",
    "host": "localhost",
    "port": "5432"
}

KEYWORDS = ['gun', 'gunsarecool', 'gunrights', 'gunviolenceprevention', 'homicide', 'gunviolence', 'firearms', 'progun', 'secondamendment', 'selfdefense', 'guncontrol', 'massshooting']

def fetch_posts(board, num_pages=10):  # Increased to fetch more pages
    all_posts = []
    for page_num in range(1, num_pages + 1):
        url = f"{API_URL}/{board}/{page_num}.json"
        print("Fetching from URL:", url)
        response = requests.get(url)

        if response.ok:
            page_data = response.json()
            for key in page_data.get('threads'):
                item = key['posts']

                for i in item:
                    if ('replies' in i.keys() and i['replies'] > 1):
                        fetch_comments(board, i['no'])

                    if ('com' not in i.keys()):
                        continue

                    post_name = i.get('name', '')  # Check if 'name' exists, otherwise use an empty string

                    all_posts.append([i['no'], i['time'], board, post_name, i['com']])

        else:
            print("Error fetching posts")
    print(len(all_posts))
    return all_posts

def fetch_comments(board, post_id):
    url = f"{API_URL}/{board}/thread/{post_id}.json"
    print("Fetching comments from URL:", url)
    response = requests.get(url)

    if response.ok:
        thread_data = response.json()
        for page in thread_data.get('posts', []):
            if 'com' in page.keys():
                if 'name' not in page.keys():
                    comments_fetched.append([post_id, page['no'], page['time'], board, 'guest', page['com']])
                else:
                    comments_fetched.append([post_id, page['no'], page['time'], board, page['name'], page['com']])
    else:
        print("Error fetching comments")

def insert_post(cur, post):
    sql = """
        INSERT INTO four_chan (post_id, board, thread_id, username, p_comment, datetime)
        VALUES (%(post_id)s, %(board)s, %(thread_id)s, %(username)s, %(p_comment)s, to_timestamp(%(datetime)s))
        ON CONFLICT (post_id) DO NOTHING;
    """

    cur.execute(sql, post)

def main():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor(cursor_factory=extras.DictCursor)

    cur.execute("CREATE TABLE IF NOT EXISTS four_chan (post_id INTEGER PRIMARY KEY, board TEXT, thread_id INTEGER, "
                "username TEXT, p_comment TEXT, datetime TIMESTAMP)")

    posts = fetch_posts("po")  # Adjust the board name as needed
    if posts:
        new_posts = []
        for post in posts:
            if any(keyword in post[4].lower() for keyword in KEYWORDS):
                new_posts.append({
                    'post_id': post[0],
                    'thread_id': post[0],
                    'board': post[2],
                    'username': post[3],
                    'p_comment': post[4],
                    'datetime': post[1]
                })

        new_comments = []
        for com in comments_fetched:
            if len(com) < 6:
                continue
            if any(keyword in com[5].lower() for keyword in KEYWORDS):
                new_comments.append({
                    'post_id': com[0],
                    'comment_id': com[1],
                    'board': com[3],
                    'username': com[4],
                    'p_comment': com[5],
                    'datetime': com[2]
                })

        print(len(new_comments))
        print(f"Inserting {len(new_posts)} new posts")

        for post in new_posts:
            insert_post(cur, post)

    conn.commit()
    cur.close()
    conn.close()
    print("Data saved to the PostgreSQL database.")

if __name__ == "__main__":
    main()


