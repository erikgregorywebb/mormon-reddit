# https://praw.readthedocs.io/en/latest/getting_started/quick_start.html
# https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
# https://github.com/reddit-archive/reddit/wiki/API
# https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps

### Authentication
import praw
import pandas as pd
import time

# create authorized instance
reddit = praw.Reddit(client_id = 'CLIENT-ID-HERE', 
                     client_secret = 'CLIENT-SECRET-HERE, 
                     user_agent = 'iphone:APP-ID-HERE:v1.0 (by /u/USERNAME-HERE)',
                     username = 'USERNAME-HERE', password = 'PASSWORD-HERE')
                     
# list four mormon subreddits
subreddits = ['latterdaysaints', 'exmormon', 'lds', 'mormon']   

### Submissions
rows = []
for item in subreddits:
    subreddit = reddit.subreddit(item)
    for submission in subreddit.new(limit = 20):
        time.sleep(1)
        try:
            submission_id = submission.id
            title = submission.title
            selftext = submission.selftext
            datetime = submission.created
            author = submission.author
            author_name = author.name
            author_id = author.id
            permalink = submission.permalink
            url = submission.url
            score = submission.score
            upvote_ratio = submission.upvote_ratio
            num_comments = submission.num_comments
            row = [item, submission_id, title, selftext, datetime, author_name, author_id, url, permalink,  score, upvote_ratio, num_comments]
            rows.append(row)
        except:
            print('Error: Submission')
    
submissions = pd.DataFrame(rows)
submissions.columns = ['subreddit', 'submission_id', 'title', 'text', 'datetime', 'author_name', 'author_id', 'url', 'permalink', 'score', 'upvote_ratio', 'num_comments']  

### Submissions
rows = []
for item in submissions['submission_id']:
    submission = reddit.submission(id = item)
    all_comments = submission.comments.list()
    for comment in all_comments:
        time.sleep(1)
        try:
            comment_id = comment.id
            author = comment.author
            comment_author = author.name
            comment_body = comment.body
            comment_creation_date = comment.created_utc
            comment_score = comment.score
            comment_is_submitter = comment.is_submitter
            comment_submission_id = comment.link_id
            comment_parent_id = comment.parent_id
            row = [item, comment_id, comment_author, comment_body, comment_creation_date, comment_score, comment_is_submitter, comment_submission_id, comment_parent_id]
            rows.append(row)
        except:
            print('Error: Comments')
        
comments = pd.DataFrame(rows)
comments.columns = ['submission_id', 'comment_id', 'comment_author', 'comment_body', 'comment_creation_date', 'comment_score', 'comment_is_submitter', 'comment_submission_id', 'comment_parent_id']

### Redditors
all_redditors = submissions['author_name'].tolist() + comments['comment_author'].tolist()
all_redditors = list(set(all_redditors))

rows = []
for item in all_redditors:
    time.sleep(1)
    try:
        author = reddit.redditor(name = item)
        name = author.name
        author_id = author.id
        comment_karma = author.comment_karma
        account_creation_date = author.created_utc
        has_verified_email = author.has_verified_email
        is_mod = author.is_mod
        row = [name, author_id, comment_karma, account_creation_date, has_verified_email, is_mod]
        rows.append(row)
    except:
        print('Error: Redditors')
    
redditors = pd.DataFrame(rows)
redditors.columns = ['name', 'author_id', 'comment_karma', 'account_creation_date', 'has_verified_email', 'is_mod']    

### Database

with pd.ExcelWriter('mormon-reddit.xlsx') as writer:  # doctest: +SKIP
    submissions.to_excel(writer, sheet_name = 'submissions')
    comments.to_excel(writer, sheet_name = 'comments')
    redditors.to_excel(writer, sheet_name = 'redditors')
print('File exported successfully.')
