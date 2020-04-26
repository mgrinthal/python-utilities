import email_lib
import configparser
import praw
import time
import sys
import prawcore
from datetime import datetime
from datetime import timedelta

configParser = configparser.RawConfigParser()
configPath = './reddit-config.txt'
configParser.read(configPath)

username = configParser.get('reddit-config', 'username')
ua_string = 'RedditPoller/0.1 by' + username

keywords = ['red wing', 'land\'s end', 'j.crew', 'j crew', 'j. crew', 'jcrew', 'banana republic',
            'bonobos', 'frank and oak', 'frank+oak', 'frank + oak', 'frank & oak', 'tall', 'allen edmond']
used_posts = []

if len(sys.argv) >= 2:
    override_time_restriction = sys.argv[1]
else:
    override_time_restriction = False

# Provide start and end times in hour minute second format
start_config = [8, 0, 0]
end_config = [22, 0, 0]

while True:

    try:

        sleep_time = 1800

        now = datetime.now()
        start_time = now.replace(
            hour=start_config[0], minute=start_config[1], second=start_config[2])
        end_time = now.replace(
            hour=end_config[0], minute=end_config[1], second=end_config[2])

        if start_time > end_time:
            print('Invalid scheduling window. Check start and end times.')
            break

        # Only run between the hours specified
        if start_time <= now <= end_time or override_time_restriction:
            # TODO: Use timestamp to delete used_posts after 24 hours
            timestamp = time.time()
            reddit = praw.Reddit(client_id=configParser.get('reddit-config', 'client-id'),
                                 client_secret=configParser.get(
                                     'reddit-config', 'secret'),
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

        if start_time > now:  # Same day, sleep until given start time
            sleep_time = (start_time - now).total_seconds() + 30
        elif end_time < now:  # Late-night, sleep until given start time next day
            start_time = start_time + timedelta(days=1)
            sleep_time = (start_time - now).total_seconds() + 30

        print('Successful iteration. Sleeping for ' +
              str(int(sleep_time / 60)) + ' minutes.')
        # Run every half an hour
        time.sleep(sleep_time)

    # Catch exceptions, sleep 60 seconds, retry
    except prawcore.exceptions.RequestException as err:
        print('Exception occurred:', err)
        time.sleep(60)
