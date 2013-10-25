from twython import Twython
import twitter_oauth_info as auth_data

class Twitter:
    '''
    Twitter class.
    '''
    def __init__(self, auth=auth_data):
        self.twitter = Twython(auth.APP_KEY, auth.APP_SECRET,
                  auth.OAUTH_TOKEN, auth.OAUTH_TOKEN_SECRET)

    def post_tweet(self, message):
        '''
        Writes message into twitter stream.
        '''
        self.twitter.update_status(status=message)

    def post(self, message):
        '''
        Writes message into console to test.
        '''
        try:
            #print message
            self.post_tweet(message)
        except Exception as e:
            print "Error:", e.message
            print "Error message:", message