# the FastReplyStreamer is a subclass of TwythonStreamer
from twython import TwythonStreamer

# the FastReplyStreamer class will use the streaming api to quickly reply to tweets.
# It will be used for filtering all tweets containing @gsgottsnack.
# This class could technically be used to reply to all kinds of tweets.
class FastReplyStreamer(TwythonStreamer):
    # this function will be called when a tweet is received
    def on_success(self, data):
        # the data variables contains a tweet
        # reply to that tweet
        self.markov.generate_reply(to_tweet=data)

    # when an error is caught
    def on_error(self, status_code, data):
        print("STREAMING API ERROR!")
        print("Status code:")
        print(status_code)
        print("Other data:")
        print(data)
        print("END OF ERROR MESSAGE")
