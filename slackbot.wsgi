#usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/stackweavers/Desktop/Workspace/slackbot/")

from slackbot import app as application
application.secretkey='123456789'

