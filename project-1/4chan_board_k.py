import requests
import psycopg2
from psycopg2 import extras

fetched = []
comments_fetched = []
API_URL = "https://a.4cdn.org"

DB_PARAMS = {
    "dbname": "reddit_data",
    "user": "kkamara1",
    "password": "12345",
    "host": "localhost",
    "port": "5432"
}

KEYWORDS = ['gun', 'gunsarecool', 'gunviolence', 'firearms', 'progun', 'secondamendment', 'selfdefense', 'guncontrol', 'massshooting']

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

    posts = fetch_posts("k")  # Adjust the board name as needed
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










"""Working 4 chan"""
# import requests
# import psycopg2
# from psycopg2 import extras
# 
# fetched = []
# comments_fetched = []
# API_URL = "https://a.4cdn.org"
# 
# DB_PARAMS = {
    # "dbname": "reddit_data",
    # "user": "kkamara1",
    # "password": "12345",
    # "host": "localhost",
    # "port": "5432"
# }
# 
# KEYWORDS = ['gun','gunsarecool', 'guns', 'firearms', 'progun','secondamendment', 'guncontrol',
              # 'massshooting',]
# 
# def fetch_posts(board, num_pages=10):
    # all_posts = []
    # for page_num in range(1, num_pages + 1):
        # url = f"{API_URL}/{board}/{page_num}.json"
        # print(url)
        # print("Fetching from URL:", url)
        # response = requests.get(url)
# 
        # if response.ok:
            # page_data = response.json()
            # for key in page_data.get('threads'):
                # # print(key['posts'])
                # item = key['posts']
# 
                # for i in item:
                    # if ('replies' in i.keys() and i['replies']>1):
                        # fetch_comments(board, i['no'])
# 
# 
# 
# 
                    # if ('com' not in i.keys()):
                        # continue
# 
                    # all_posts.append([i['no'],i['time'],board,i['name'], i['com']])
# 
        # else:
            # print("Error fetching posts")
    # print(len(all_posts))
    # return all_posts
# 
# def fetch_comments(board, post_id):
    # url = f"{API_URL}/{board}/thread/{post_id}.json"
    # print("Fetching comments from URL:", url)
    # response = requests.get(url)
# 
    # if response.ok:
        # thread_data = response.json()
        # for page in thread_data.get('posts', []):
            # if 'com' in page.keys():
                # if 'name' not in page.keys():
                    # comments_fetched.append([post_id,page['no'],page['time'],board, 'guest', page['com']])
                # else:
                # # print(page.keys())
                    # comments_fetched.append([post_id,page['no'],page['time'],board, page['name'], page['com']])
    # else:
        # print("Error fetching comments")
# 
# 
# def insert_post(cur, post):
    # sql = """
        # INSERT INTO four_chan (post_id, board, thread_id, username, p_comment, datetime)
        # VALUES (%(post_id)s, %(board)s, %(thread_id)s, %(username)s, %(p_comment)s, to_timestamp(%(datetime)s))
        # ON CONFLICT (post_id) DO NOTHING;
    # """
# 
    # cur.execute(sql, post)
# 
# def main():
    # conn = psycopg2.connect(**DB_PARAMS)
    # cur = conn.cursor(cursor_factory=extras.DictCursor)
# 
    # cur.execute("CREATE TABLE IF NOT EXISTS four_chan (post_id INTEGER PRIMARY KEY, board TEXT, thread_id INTEGER, username TEXT, p_comment TEXT, datetime TIMESTAMP)")
# 
    # posts = fetch_posts("k")  # Adjust the board name as needed
    # if posts:
        # # existing_ids = {row[0] for row in cur.execute("SELECT post_id FROM four_chan_data")}
# 
        # new_posts = []
        # for post in posts:
            # # print(post)
            # # if post['no'] not in existing_ids:
            # if any(keyword in post[4].lower() for keyword in KEYWORDS):
                # new_posts.append({
                    # 'post_id': post[0],
                    # 'thread_id':post[0],
                    # 'board': post[2],
                    # # 'thread_id': post.get('thread_num', ''),
                    # 'username': post[3],
                    # 'p_comment': post[4],
                    # 'datetime': post[1]
                # })
        # new_comments = []
        # for com in comments_fetched:
            # if (len(com) <6):
# 
                # continue
            # # print(post)
            # # if post['no'] not in existing_ids:
            # if any(keyword in com[5].lower() for keyword in KEYWORDS):
                # new_comments.append({
                    # 'post_id': com[0],
                    # 'comment_id': com[1],
                    # # 'thread_id':com[2],
                    # 'board': com[3],
                    # # 'thread_id': post.get('thread_num', ''),
                    # 'username': com[4],
                    # 'p_comment': com[5],
                    # 'datetime': com[2]
                # })
        # print(len(new_comments))
# 
# 
        # print(f"Inserting {len(new_posts)} new posts")
# 
        # for post in new_posts:
            # insert_post(cur, post)
# 
    # conn.commit()
    # cur.close()
    # conn.close()
    # print("Data saved to the PostgreSQL database.")
# 
# if __name__ == "__main__":
    # main()
































# import requests
# import psycopg2
# from psycopg2 import extras

# API_URL = "https://a.4cdn.org"

# DB_PARAMS = {
#     "dbname": "reddit_data",
#     "user": "kkamara1",
#     "password": "12345",
#     "host": "localhost",
#     "port": "5432"
# }

# KEYWORDS = ['Gun Politics', 'Gun Culture', 'firearms', 'second amendment', 'NRA', 'Pro-gun']

# def fetch_posts(board, num_pages=3):
#     all_posts = []
#     for page_num in range(1, num_pages + 1):
#         url = f"{API_URL}/{board}/{page_num}.json"
#         print(url)
#         print("Fetching from URL:", url)
#         response = requests.get(url)

#         if response.ok:
#             page_data = response.json()
#             for post in page_data.get('posts', []):
#                 if 'com' in post:
#                     all_posts.append(post)
#                 else:
#                     print("Post has no 'com' field:", post)
#         else:
#             print("Error fetching posts")

#     return all_posts

# def insert_post(cur, post):
#     sql = """
#         INSERT INTO four_chan_data (post_id, board, thread_id, username, p_comment, datetime)
#         VALUES (%(post_id)s, %(board)s, %(thread_id)s, %(username)s, %(p_comment)s, to_timestamp(%(datetime)s))
#         ON CONFLICT (post_id) DO NOTHING;
#     """

#     cur.execute(sql, post)

# def main():
#     conn = psycopg2.connect(**DB_PARAMS)
#     cur = conn.cursor(cursor_factory=extras.DictCursor)

#     cur.execute("CREATE TABLE IF NOT EXISTS four_chan_data (post_id INTEGER PRIMARY KEY, board TEXT, thread_id INTEGER, username TEXT, p_comment TEXT, datetime TIMESTAMP)")

#     posts = fetch_posts("po")  # Adjust the board name as needed
#     print(posts)
#     if posts:
#         existing_ids = {row[0] for row in cur.execute("SELECT post_id FROM four_chan_data")}

#         new_posts = []
#         for post in posts:
#             if post['no'] not in existing_ids:
#                 if 'com' in post and any(keyword in post['com'].lower() for keyword in KEYWORDS):
#                     new_posts.append({
#                         'post_id': post['no'],
#                         'board': post.get('board', ''),
#                         'thread_id': post.get('thread_num', ''),
#                         'username': post.get('name', ''),
#                         'p_comment': post.get('com', ''),
#                         'datetime': post.get('time', '')
#                     })

#         print(f"Inserting {len(new_posts)} new posts")

#         for post in new_posts:
#             insert_post(cur, post)

#     conn.commit()
#     cur.close()
#     conn.close()
#     print("Data saved to the PostgreSQL database.")

# if __name__ == "__main__":
#     main()




# import requests
# import psycopg2
# from psycopg2 import extras

# API_URL = "https://a.4cdn.org"

# DB_PARAMS = {
#   "dbname": "reddit_data",
#   "user": "kkamara1",
#   "password": "12345",
#   "host": "localhost",
#   "port": "5432"
# }

# KEYWORDS = ['Gun Politics', 'Gun Culture', 'firearms', 'second amendment', 'NRA', 'Pro-gun']

# def fetch_posts(board):
#   url = f"{API_URL}/{board}/catalog.json"
#   print("Fetching from URL:", url)  # Add this line to print the constructed URL
#   response = requests.get(url)

#   if response.ok:
#     catalog = response.json()
#     posts = []
#     for page in catalog:
#       for thread in page['threads']:
#         posts.extend(thread.get('posts', []))
#     return posts
#   else:
#     print("Error fetching posts")
#     return None

# def insert_post(cur, post):
#   sql = """
#     INSERT INTO four_chan (post_id, board, thread_id, username, p_comment, datetime)
#     VALUES (%(post_id)s, %(board)s, %(thread_id)s, %(username)s, %(p_comment)s, to_timestamp(%(datetime)s))
#     ON CONFLICT (post_id) DO NOTHING;
#   """

#   cur.execute(sql, post)

# def main():

#   conn = psycopg2.connect(**DB_PARAMS)
#   cur = conn.cursor(cursor_factory=extras.DictCursor)  

#   cur.execute("CREATE TABLE IF NOT EXISTS four_chan (post_id INTEGER PRIMARY KEY, board TEXT, thread_id INTEGER, username TEXT, p_comment TEXT, datetime TIMESTAMP)")

#   posts = fetch_posts("po")
#   print(posts)
#   if posts:
#     existing_ids = {row[0] for row in cur.execute("SELECT post_id FROM four_chan")}

#     new_posts = []
#     for post in posts:
#       if post['no'] not in existing_ids:  
#         if any(keyword in post['com'].lower() for keyword in KEYWORDS):
#           new_posts.append(post)
    

#     print(f"Inserting {len(new_posts)} new posts")

#     for post in new_posts:
#       insert_post(cur, post)

#   conn.commit()
#   cur.close()
#   conn.close()

# if __name__ == "__main__":
#   main()


# import requests
# import psycopg2
# from psycopg2 import extras

# API_BASE_URL = "https://a.4cdn.org"

# db_params = {
#     "dbname": "reddit_data",  # Replace with your PostgreSQL database name
#     "user": "kkamara1",       # Replace with your PostgreSQL username
#     "password": "12345",      # Replace with your PostgreSQL password
#     "host": "localhost",      # Change if your database is hosted elsewhere
#     "port": "5432"            # Change if your PostgreSQL port is different
# }

# def create_4chan_table_if_not_exists(conn):
#     cur = conn.cursor()
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS four_chan_data (
#             board TEXT,
#             thread_id INTEGER,
#             post_id INTEGER,
#             username TEXT,
#             p_comment TEXT,
#             datetime TIMESTAMP
#         );
#     """)
#     conn.commit()

# def fetch_4chan_board_posts(board):
#     url = f"{API_BASE_URL}/{board}/catalog.json"
#     response = requests.get(url)

#     if response.status_code == 200:
#         catalog = response.json()
#         posts = []
#         for page in catalog:
#             for thread in page['threads']:
#                 posts.extend(thread.get('posts', []))
#         return posts
#     else:
#         print("Failed to fetch data from 4chan API.")
#         return None

# def save_posts_to_postgresql(posts):
#     conn = psycopg2.connect(**db_params)
#     create_4chan_table_if_not_exists(conn)

#     cur = conn.cursor(cursor_factory=extras.DictCursor)
#     existing_posts = set()

#     cur.execute('SELECT post_id FROM four_chan_data')
#     rows = cur.fetchall()
#     existing_posts = set(row[0] for row in rows) if rows else set()

#     new_posts = []
#     for post in posts:
#         post_data = {
#             'board': post['board'],
#             'thread_id': post['no'],
#             'post_id': post['no'],
#             'username': post.get('name', ''),
#             'p_comment': post.get('com', ''),
#             'datetime': post['time']
#         }

#         # Check if the post is unique and contains any of the keywords
#         if post_data['post_id'] not in existing_posts:
#             keywords = ['Gun Politics', 'Gun Culture', 'firearms', 'second amendment', 'NRA', 'Pro-gun']
#             if any(keyword.lower() in post_data['p_comment'].lower() for keyword in keywords):
#                 new_posts.append(post_data)
#                 existing_posts.add(post_data['post_id'])

#     for post in new_posts:
#         try:
#             cur.execute("""
#                 INSERT INTO four_chan_data (board, thread_id, post_id, username, p_comment, datetime)
#                 VALUES (%(board)s, %(thread_id)s, %(post_id)s, %(username)s, %(p_comment)s, to_timestamp(%(datetime)s));
#                 """, post)
#         except Exception as e:
#             print("Error inserting data:", e)

#     conn.commit()
#     print(f"Successfully saved {len(new_posts)} unique posts containing keywords to the database.")

# if __name__ == "__main__":
#     board_name = "k"  # Replace with the desired board name

#     posts = fetch_4chan_board_posts(board_name)

#     if posts:
#         save_posts_to_postgresql(posts)
