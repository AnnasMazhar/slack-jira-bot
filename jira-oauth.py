import requests
from oauthlib.oauth1 import SIGNATURE_RSA
from requests_oauthlib import OAuth1Session
from jira.client import JIRA

def read(file_path):
    """ Read a file and return it's contents. """
    with open(file_path) as f:
        return f.read()

# The Consumer Key created while setting up the "Incoming Authentication" in
# JIRA for the Application Link.
CONSUMER_KEY = ''

# The contents of the rsa.pem file generated (the private RSA key)
RSA_KEY = read('/home/stackweavers/Desktop/Workspace/slackbot/bot auth')

# The URLs for the JIRA instance
JIRA_SERVER = 'https://acitjira.atlassian.net'
REQUEST_TOKEN_URL = JIRA_SERVER + '/plugins/servlet/oauth/request-token'
AUTHORIZE_URL = JIRA_SERVER + '/plugins/servlet/oauth/authorize'
ACCESS_TOKEN_URL = JIRA_SERVER + '/plugins/servlet/oauth/access-token'


# Step 1: Get a request token

oauth = OAuth1Session(CONSUMER_KEY, signature_type='auth_header', 
                      signature_method=SIGNATURE_RSA, rsa_key=RSA_KEY)
request_token = oauth.fetch_request_token(REQUEST_TOKEN_URL)


print("STEP 1: GET REQUEST TOKEN")
print("  oauth_token={}".format(request_token['oauth_token']))
print("  oauth_token_secret={}".format(request_token['oauth_token_secret']))
print("\n")


# Step 2: Get the end-user's authorization

print("STEP2: AUTHORIZATION")
print("  Visit to the following URL to provide authorization:")
print("  {}?oauth_token={}".format(AUTHORIZE_URL, request_token['oauth_token']))
print("\n")

while input("Press any key to continue..."):
    pass


# Step 3: Get the access token

access_token = oauth.fetch_access_token(ACCESS_TOKEN_URL)

print("STEP2: GET ACCESS TOKEN")
print("  oauth_token={}".format(access_token['oauth_token']))
print("  oauth_token_secret={}".format(access_token['oauth_token_secret']))
print("\n")


# Now you can use the access tokens with the JIRA client. Hooray!

jira = JIRA(options={'server': JIRA_SERVER}, oauth={
    'access_token': access_token['oauth_token'],
    'access_token_secret': access_token['oauth_token_secret'],
    'consumer_key': CONSUMER_KEY,
    'key_cert': RSA_KEY
})

# print all of the project keys just as an exmaple
for project in jira.projects():
    print(project.key)
