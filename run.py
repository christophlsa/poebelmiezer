import sys
import json
from twitter import OAuth
from poebelmiezer import Poebelmiezer

try:
    with open('settings.json', 'r') as f:
        settings = json.load(f)

    oauth = OAuth(settings['token'], settings['token_secret'], settings['consumer_key'], settings['consumer_secret'])
except FileNotFoundError:
    sys.stderr.write('You have to create the settings.json file with the OAuth token/keys.\n')
    exit(1)
except ValueError:
    sys.stderr.write('The settings file couldn\'t parse. The json has an error.\n')
    exit(1)
except KeyError as e:
    sys.stderr.write('The option "{}" in the settings file is missing.\n'.format(e.args[0]))
    exit(1)

p = Poebelmiezer(oauth)

p.search_new_follower()
p.look_for_followfriday(5)

print("to follow: {}".format(p.to_follow))

p.follow_all()
