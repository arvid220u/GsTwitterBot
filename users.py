# -*- coding: utf-8 -*-
# this class provides the Users class, which sorts all the followers, and
# checks if there are any new followers
import time
# import the twython api
import twythonaccess

# import random, so every follower_greeting is not always the same
from random import randint

class Users:
    # followers array (contains full user objects)
    followers = []
    # followfollowers array
    followfollowers = []
    # followfollowfollowers array
    #followfollowfollowers = []
    # The tweets arrays
    followers_tweets = []
    followfollowers_tweets = []

    # Initializer
    def __init__(self):
        # Initialize the follower arrays
        self.followers = self.get_followers_array()
        self.followfollowers = self.get_followfollowers_array()
        #self.followfollowfollowers = self.getFollowfollowfollowersArray()
        # Get all the tweets
        self.followers_tweets = self.get_tweets(self.followers)
        self.followfollowers_tweets = self.get_tweets(self.followfollowers)


    # Return followers arrays
    def get_followers_array(self):
        # get the followers array, but first check requests
        twythonaccess.check_if_requests_are_maximum(13)
        followers = twythonaccess.authorize().get_followers_list(screen_name=twythonaccess.screen_name)
        print("gotten followers array")
        return followers["users"]

    def get_followfollowers_array(self):
        # get the followers
        followfollowers = []
        # loop through each follower, and add their followers to
        # the followfollowers list
        for follower in self.followers:
            print("getting followers for follower: " + follower["name"])
            twythonaccess.check_if_requests_are_maximum(13)
            this_followers_follower = twythonaccess.authorize().get_followers_list(user_id=follower["id"])
            followfollowers.extend(this_followers_follower["users"])

        # add goranhagglund to the followfollower list, because he is funny
        twythonaccess.check_if_requests_are_maximum(170)
        followfollowers.append(twythonaccess.authorize().show_user(screen_name="goranhagglund"))

        # check if any followfollower already is in the follower id,
        # if so, remove the follower from the followfollower array
        """
        for followfollower in followfollowers:
            for follower in followers:
                if followfollower["id"] == follower["id"]:
                    followfollowers.remove(followfollower)
            for anotherFollowfollower in followfollowers:
                if followfollower["id"] == anotherFollowfollower["id"]:
                    followfollower.remove(anotherFollowfollower)
        """
        # now return the followfollowers array
        return followfollowers

    # Return the tweets for each follower (may take long time,
    # because of the requests limit)
    def get_tweets(self, followers_array):

        print("getting tweets")

        tweets = []

        for user in followers_array:
            # check so user isn't protected
            if not user["protected"]:
                # Get this follower's tweets, but first check limit
                twythonaccess.check_if_requests_are_maximum(170)
                this_users_tweets = twythonaccess.authorize().get_user_timeline(user_id=user["id"], trim_user=True, include_rts=False)
                tweets.extend(this_users_tweets)
                print("got tweets of user " + user["name"])
            else:
                print("user " + user["name"] + " is protected.")
        # remove all tweets which are not marked as Swedish
        """for tweet in tweets:
            if tweet["lang"] != "sv":
                tweets.remove(tweet)
                print("tweet is not Swedish: " + tweet["text"])
                time.sleep(0.5)"""

        return tweets


    # This function gets new tweets for the followers and fllowfollowers
    # It will update the tweets arrays, and also answer
    # new tweets from the followers
    def check_new_tweets(self):
        # The new arrays
        new_followers_tweets = self.get_tweets(self.followers)
        new_followfollowers_tweets = self.get_tweets(self.followfollowers)

        # Check if there's any new tweet by any follower, and answer
        # it. Only answer one tweet per user per time this function
        # is called. Quote the original tweet.
        answered_users_ids = []
        # the tweets ids
        old_tweets_ids = []
        for tweet in self.followers_tweets:
            old_tweets_ids.append(tweet["id"])
        for new_followers_tweet in new_followers_tweets:
            if new_followers_tweet["id"] not in old_tweets_ids:
                # only answer 50% of tweets, or if there was a mention of gs
                random_number = randint(1,2)
                if (random_number == 1 and new_followers_tweet["user"]["id"] not in answered_users_ids) or "gs" in new_followers_tweet["text"]:
                    # if @gsgottsnack is contained in the tweet, then don't reply here, as that will be taken care of in FastReplyStreamer
                    if not "@gsgottsnack" in new_followers_tweet["text"]:
                        # don't reply to the same user twice if no gs
                        answered_users_ids.append(new_followers_tweet["user"]["id"])
                        # reply to the tweet
                        self.markov.generate_reply(to_tweet=new_followers_tweet)

        # update the self attrbutes
        self.followers_tweets = new_followers_tweets
        self.followfollowers_tweets = new_followfollowers_tweets



    # This function gets new followers and followfollowers arrays
    # It updates the self attributes, and if there's a new user in the arrays,
    # welcomes them with a tweet
    def check_new_followers(self):

        print("getting new followers")

        # The new arrays
        new_followers = self.get_followers_array()
        new_followfollowers = self.get_followfollowers_array()

        # Check if there's any difference, and send a tweet about the follower
        # follower ids
        old_followers_ids = []
        for old_follower in self.followers:
            old_followers_ids.append(old_follower["id"])
        for new_follower in new_followers:
            if new_follower["id"] not in old_followers_ids:
                # greet new follower
                while True:
                    # get a random adjective
                    adjective = ""
                    randomNumber = randint(1,4)
                    if randomNumber % 2 == 0:
                        # 50%
                        adjective = "Mycket"
                    elif randomNumber == 1:
                        # 25%
                        adjective = "Ganska"
                    elif randomNumber == 3:
                        # 25%
                        adjective = "Lite"
                    # compose the tweet
                    tweet = "Ny följare idag: @" + new_follower['screen_name'] + ". " + adjective + " gs."
                    if twythonaccess.send_tweet(tweet):
                        print("greeting new follower with tweet: " + tweet)
                        # Also add this user's tweets to the tweets array,
                        # so the bot won't answer all of the user's tweets
                        twythonaccess.check_if_requests_are_maximum(170)
                        this_users_tweets = twythonaccess.authorize().get_user_timeline(user_id=new_follower["id"], trim_user=True, include_rts=False)
                        self.followers_tweets.extend(this_users_tweets)
                        break

        # update the original arrays
        self.followers = new_followers
        self.followfollowers = new_followfollowers
