from twitter import Twitter, TwitterHTTPError

"""class for twitter follower management"""
class Poebelmiezer:
    """
    :param oauth: twitter.OAuth object for twitter
    """
    def __init__(self, oauth):
        self.to_follow = {}
        self.all_follower = []
        self.t = Twitter(auth = oauth)

    """follow all users found with the other functions (follower list)"""
    def follow_all(self):
        for f in self.to_follow:
            self.t.friendships.create(user_id=f['id'])
        self.to_follow.clear()

    """go through all follower and save the non followed and non protected users to the follower list"""
    def search_new_follower(self):
        self.fetch_all_follower()

        for f in self.all_follower:
            if not f['following'] and not f['protected']:
                self.to_follow.add(f['id'])

    """fetch all follower and save them in a list
    :param cursor: a cursor for the next page for the api (to begin set to None)
    """
    def fetch_all_follower(self, cursor=None):
        try:
            if cursor:
                results = self.t.followers.list(skip_status=True, include_user_entities=False, cursor=cursor)
            else:
                self.all_follower.clear()
                results = self.t.followers.list(skip_status=True, include_user_entities=False)
        except TwitterHTTPError as e:
            if e.e.code is 429:
                print('Rate limit exceeded')
            else:
                raise e
            exit()

        self.all_follower.extend(results['users'])

        if results['next_cursor'] != 0:
            self.fetch_all_follower(results['next_cursor'])

    """calls get_ff_suggestions n times
    :param count: count of fcuntion calls
    """
    def look_for_followfriday(self, count=1):
        max_id = self.get_ff_suggestions() - 1
        for i in range(count - 1):
            max_id = self.get_ff_suggestions(max_id) - 1

    """fetch the timeline, look for tweets with hashtag #ff and save all suggested users to the follow list
    :param max_id: maximum id of tweets to fetch (older or equal tweets)
    :returns: the id of the last fetched tweet
    """
    def get_ff_suggestions(self, max_id=None):
        try:
            if max_id:
                timeline = self.t.statuses.home_timeline(include_entities=True, max_id=max_id)
            else:
                timeline = self.t.statuses.home_timeline(include_entities=True)
        except TwitterHTTPError as e:
            if e.e.code is 429:
                print('Rate limit exceeded')
            else:
                raise e
            exit()

        for tweet in timeline:
            if 'retweeted_status' not in tweet and '#ff' in tweet['text']:
                if 'entities' in tweet and 'user_mentions' in tweet['entities']:
                    for user_mention in tweet['entities']['user_mentions']:
                        self.to_follow.add(user_mention['id'])

        return timeline[-1]['id']

