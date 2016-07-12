#!/usr/bin/env python

# Usage:
#  slack-members.py <channel id> > <channel id>-members.csv
# Find a list of people who are members of a Slack channel
#
# Info needed:
# + API authentication token for this Slack organization
# ++ (OAuth requires a callback URL, and this isn't a web app so the token must be a testing key.)
#
# Method:
# + Retrieve users list for this slack team: https://api.slack.com/methods/users.list (list of https://api.slack.com/types/user)

# Future consideration -- limit scope to a single channel or group
# + Retrieve channels list: https://api.slack.com/methods/channels.list
# + Retrieve group list (private channels): https://api.slack.com/methods/groups.list
# ++ add those to the list of channels for which we could possibly want to view the membership
# + If a channel id wasn't provided, list all the channel/group id numbers along with each channel's name
# + If a channel/group ID *was* provided

# API exploration
# >>> import slacker
# >>> slack = slacker.Slacker('<API token goes here>')
# >>> users = slack.users.list()
# >>> users.body
# ... list of user objects https://api.slack.com/types/user
# Useful fields of users.body['members'][n]: 
#  ['deleted'], ['id'], ['name'], ['profile']['real_name'], ['profile']['email']

# No-longer necessary API exploration (will be needed for future user list by channel/group):
# >>> channels = slack.channels.list()
# >>> dir(channels)
# ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'body', 'error', 'raw', 'successful']
# >>> channels.body
# ... dictionary that looks like a list of channels under the key 'channels'
# >>> channels.body['channels'][0]['members']
# ['U1M2EJEHL', 'U1M3H0KQC', 'U1M4K2ZK6', ... etc
# Users listed only by ID-- need a way to dereference those
#
#
# Private channels are handled through a different API
# >>> groups = slack.groups.list()
# >>> dir(groups)
# ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'body', 'error', 'raw', 'successful']
# >>> groups.body
# ... similar to the above channels.body, but uses the key 'groups' and doesn't have an 'ok' key entry

import os
import warnings
import slacker

# The API key is kept in a local file so I don't do something silly like upload my private API key to github.
# Borrowed from https://github.com/rhgrant10/Groupy (also GPL)
def _attempt_to_load_apikey():
	filepath = os.path.expanduser(KEY_LOCATION)
	try:
		with open(filepath, 'r') as f:
			API_KEY = f.read().strip()
			return API_KEY
	except IOError as e:
		API_KEY = None
		if e.errno != 2:
			warnings.warn(
				'key file {} exists but could not be opened: {}'.format(
				KEY_LOCATION,
				str(e)))


KEY_LOCATION = '~/.slacker.key'
API_KEY = _attempt_to_load_apikey()

slack = slacker.Slacker(API_KEY)
users = slack.users.list()
print("UID,Name,Real Name,E-mail Address,Deleted")
for user in users.body['members']:
	print("\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"" % (user['id'], user['name'], user['profile']['real_name'], user['profile']['email'],user['deleted']) )
	
