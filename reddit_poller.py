import email_lib, requests, requests.auth, configparser, praw

configParser = configparser.RawConfigParser()
configPath = './reddit-config.txt'
configParser.read(configPath)

username = configParser.get('reddit-config', 'username')
ua_string = 'RedditPoller/0.1 by' + username

reddit = praw.Reddit(client_id=configParser.get('reddit-config', 'client-id'),
                     client_secret=configParser.get('reddit-config', 'secret'),
                     user_agent=ua_string)

print(reddit.read_only)
