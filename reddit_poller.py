import email_lib, configparser, praw, time, sys
from datetime import datetime

configParser = configparser.RawConfigParser()
configPath = './reddit-config.txt'
configParser.read(configPath)

username = configParser.get('reddit-config', 'username')
ua_string = 'RedditPoller/0.1 by' + username

keywords = ['red wing', 'land\'s end', 'j.crew', 'j crew', 'j. crew', 'banana republic', 'bonobos', 'frank and oak', 'frank+oak', 'frank & oak', 'tall', 'allen edmonds']
used_posts = []

if len(sys.argv) >= 2:
  override_time_restriction = sys.argv[1]
else:
  override_time_restriction = False

while True:

  now = datetime.now()
  start_time = now.replace(hour=8, minute=0, second=0)
  end_time = now.replace(hour=22, minute=0, second=0)

  # Only run between the hours of 8am and 10pm
  if start_time <= now <= end_time or override_time_restriction:
    print('running')
    # TODO: Use timestamp to delete used_posts after 24 hours
    timestamp = time.time()
    reddit = praw.Reddit(client_id=configParser.get('reddit-config', 'client-id'),
                         client_secret=configParser.get('reddit-config', 'secret'),
                         user_agent=ua_string)

    fmf = reddit.subreddit('frugalmalefashion')

    keyword_posts = []
    top_posts = []

    for submission in fmf.top('day'):
      # Check only posts we haven't already used
      if submission.id not in used_posts:
        # Get keyword posts with high ratings
        if submission.score > 100 and any(word in submission.title.lower() for word in keywords):
          keyword_posts.append(submission)
        # Get high-rated posts
        elif submission.score > 100:
          top_posts.append(submission)
        # Get keyword posts
        elif any(word in submission.title.lower() for word in keywords):
          keyword_posts.append(submission)

    message_body = ''
    if keyword_posts:
      message_body = '<b>Keyword Matches:</b><br/><br/>'
      for post in keyword_posts:
        message_body += '<a href="' + post.url + '">' + post.title + '</a><br/><br/>'
        used_posts.append(post.id)

    if top_posts:
      message_body += '<br/><br/><b>Top Posts:</b><br/><br/>'
      for post in top_posts:
        message_body += '<a href="' + post.url + '">' + post.title + '</a><br/><br/>'
        used_posts.append(post.id)

    # Only send an email if there are new posts
    if keyword_posts or top_posts:
      email_lib.send('FMF Digest', message_body)

  # Run every half an hour
  time.sleep(1800)
