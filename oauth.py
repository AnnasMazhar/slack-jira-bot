import os
import json
from flask import Flask, request
from slackclient import SlackClient

client_id = os.environ["SLACK_CLIENT_ID"]
client_secret = os.environ["SLACK_CLIENT_SECRET"]
oauth_scope = os.environ["SLACK_BOT_SCOPE"]

app = Flask(__name__)


@app.route("/begin_auth", methods=["GET"])
def pre_install():
    path = '''
      <a href="https://slack.com/oauth/authorize?scope={0}&client_id={1}&redirect_uri=http://127.0.0.1:5000/finish_auth">
          Add to Slack
      </a>
    '''.format(oauth_scope, client_id)
    return path


@app.route("/finish_auth", methods=["GET", "POST"])
def post_install():

    # Retrieve the auth code from the request params
    auth_code = request.args['code']

    # An empty string is a valid token for this request
    sc = SlackClient("")

    # Request the auth tokens from Slack
    auth_response = sc.api_call(
    "oauth.access",
    client_id=client_id,
    client_secret=client_secret,
    code=auth_code
    )

    return json.dumps(auth_response)

    os.environ["SLACK_USER_TOKEN"] = auth_response['access_token']
    os.environ["SLACK_BOT_TOKEN"] = auth_response['bot']['bot_access_token']
    return "Auth Complete!"


if __name__ == "__main__":
    app.run(debug=True)
