import email_lib, requests, requests.auth, configparser

configParser = configparser.RawConfigParser()
configPath = './reddit-config.txt'
configParser.read(configPath)

username = configParser.get('reddit-config', 'username')

client_auth = requests.auth.HTTPBasicAuth(configParser.get('reddit-config', 'client-id'), configParser.get('reddit-config', 'secret'))
post_data = {"grant_type": "password", "username": username, "password": configParser.get('reddit-config', 'password')}
ua_string = 'RedditPoller/0.1 by' + username
headers = {"User-Agent": ua_string}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
response = response.json()

authorization = 'bearer ' + response['access_token']

headers = {"Authorization": authorization, "User-Agent": ua_string}
# Can now make requests with the OAuth token
