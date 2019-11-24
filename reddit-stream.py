import praw
import time
import sqlite3
import traceback

# create authorized instance
reddit = praw.Reddit(client_id = 'CLIENT-KEY-HERE',
                     client_secret = 'CLIENT-SECRET-HERE',
                     user_agent = 'iphone:APP-ID-HERE:v1.0 (by /u/USERNAME-HERE)',
                     username = 'USERNAME-HERE', password = 'USERNAME-HERE!')

# connect to the sqlite database
dbConn = sqlite3.connect("mormon_reddit.db")

# get a database cursor to execute commands against
cur = dbConn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS all_comments (
        subreddit VARCHAR(30) NOT NULL,
        datetime VARCHAR(30) NOT NULL,
        username VARCHAR(30) NOT NULL,
        comment_id VARCHAR(30) NOT NULL
    )
''')

dbConn.commit()

def insertComment(subreddit, datetime, username, comment_id):
    cur = dbConn.cursor()
    try:
        cur.execute('''
            INSERT INTO all_comments
            (subreddit, datetime, username, comment_id)
            VALUES (?, ?, ?, ?)
    ''', (subreddit, datetime, username, comment_id))
    except sqlite3.IntegrityError:
        return False

    dbConn.commit()
    return True


def commentExists(comment_id):
    cur = dbConn.cursor()

    result = cur.execute('''
        SELECT comment_id
        FROM all_comments
        WHERE comment_id = ?
    ''', (comment_id,))

    if result.fetchone():
        return True
    else:
        return False

while True:
    try:
        for comment in reddit.subreddit('latterdaysaints+mormon+lds+exmormon').stream.comments():
            if not commentExists(comment.id):
                insertComment(comment.subreddit.fullname, comment.created, comment.author.name, comment.id)
                print(comment.subreddit, comment.created, comment.author.name, comment.id)
    except Exception as err:
        print(traceback.format_exc())
    finally:
        time.sleep(60)
