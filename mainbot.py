# Import the twython module
from . import twythonaccess
# import time and sys
import time
# import the users class
from .users import Users
# import markov
from .markov import Markov
# import fastreplystreamer
from .fastreplystreamer import FastReplyStreamer
# import apikeys to authenticate streamer
from . import apikeys
# import Thread to be able to run concurrently
from threading import Thread
# randint for the tweet interval
from random import randint



# the main function will be called when this script is called in terminal
# the bash command "python3 mainbot.py" will call this function
def main():

    # first setup users and markov objects
    # set this up with error handling
    while True:
        try:
            setup()
            break
        except Exception as exception:
            print(exception)
            print("will sleep for 1 hour to avoid exception")
            time.sleep(60*60)
            print("exception sleep in setup now finished; retrying setup")
    
    # create two threads, which will call reply_streamer and tweet_loop
    # use threads to make these threads be able to run concurrently
    reply_streamer_thread = Thread(target = reply_streamer)
    tweet_loop_thread = Thread(target = tweet_loop)
    # start both threads
    reply_streamer_thread.start()
    tweet_loop_thread.start()
    # these threads will run infinitely




# create the global markov and users instances
def setup():
    global markov, users
    # Declare all the global variabes which will be used

    # The users object will contain
    # the two arrays: followers and followfollowers
    # This instantiation will also start the process of checking for new followers,
    # and in those cases greet them
    users = Users()
    print("initialized users")
    # instantiate the markov object
    #markov = Markov(users.followers_tweets + users.followfollowers_tweets)

    # do this instead: mix the followers' tweets with tweets from goranhagglund and rossa_d
    twythonaccess.check_if_requests_are_maximum(170)
    twythonaccess.check_if_requests_are_maximum(170)
    ghAndRdTweets = users.get_tweets([
        twythonaccess.authorize().show_user(screen_name="goranhagglund"),
        twythonaccess.authorize().show_user(screen_name="rossa_d")])

    markov = Markov(users.followers_tweets + ghAndRdTweets + users.followfollowers_tweets)
    print("initialized markov")

    # the user shoud be able to reference the markov object
    users.markov = markov


    print("setup complete")




# this function will be executed in one thread, and tweet_loop on the other
# purpose to isolate this in streaming api is to reply to all tweets mentioning self quickly
def reply_streamer():
    print("starting registering for streaming api")
    # initialize the fastreplystreamer
    streamer = FastReplyStreamer(apikeys.CONSUMER_KEY, apikeys.CONSUMER_SECRET, apikeys.ACCESS_TOKEN, apikeys.ACCESS_TOKEN_SECRET) 
    # pass this markov instance to the streamer, so it will be able to generate replies
    streamer.markov = markov
    # start the filter
    # nest it in error handling
    while True:
        try:
            streamer.statuses.filter(track=("@" + twythonaccess.screen_name))
        except Exception as exception:
            # print the exception and then sleep for an hour
            # the sleep will reset rate limit
            # if twitter's servers were down, they may be up after the sleep
            # after the sleep, the filter function will be called anew
            print(exception)
            print("will sleep for 1 hour to avoid exception")
            time.sleep(60*60)
            print("finished sleep after exception in streaming api. will now start anew")


# the run loop, which will continue in infinity
def tweet_loop():
    while True:
        print("start loop")

        
        # the try is for error handling
        # if any of the twython methods (nested or not) raise an exception,
        # then it will be caught in this except clause
        # the except clause will do nothing but sleep for a while,
        # and then continue with the loop
        try:

            # send tweet
            while True:
                # generate new tweet
                tweet = markov.generate_tweet()
                print("tweet generated: " + tweet)
                if twythonaccess.send_tweet(tweet):
                    # the generated tweet is okay
                    print("tweet approved or passed")
                    break

            # sleeping point, if need for sleep
            # sleep for one day
            # make the sleep somewhat randomized
            # can range from 5 minutes to 3 days
            # make the distribution curve peak at 24 hours
            # get a random integer between 5 and 2.25*24*60, representing minutes
            # based on calculations, do first loop 5 times and second loop once
            min_sleep = 5
            max_sleep = 2.25*24*60
            sleep_minutes = randint(min_sleep, max_sleep)
            for i in range(0,4):
                # if the value isn't in the specified range, then regenerate the value
                # this will increase the statistical probability of the value falling in the range, while not limiting the value directly
                # first limit the value in a close range, then in a bigger range, order is important
                # this will make the curve like a double-sided stairway with three levels, the middle level being the widest
                if sleep_minutes < 23*60 or sleep_minutes > 27*60:
                    sleep_minutes = randint(min_sleep, max_sleep)
            # second loop, wider, designed to catch almost all values
            for i in range(0,1):
                if sleep_minutes < 6*60 or sleep_minutes > 46*60:
                    sleep_minutes = randint(min_sleep, max_sleep)

            print("will sleep for " + str(sleep_minutes) + " minutes")
            time.sleep(sleep_minutes * 60)
            print("has slept for " + str(sleep_minutes) + " minutes")
            
            # temporary sleep
            time.sleep(60*60)

            # update the users followers
            users.check_new_followers()
            print("updated followers")

            #print("followers:")
            #for follower in users.followers:
                #print(follower["screen_name"])
                #time.sleep(1)
            #print "followfollowers:"
            #for followfollower in users.followfollowers:
                #print(followfollower["screen_name"])
                #time.sleep(1)

            # update the tweets
            users.check_new_tweets()
            print("updated tweets")

            #print("follower's tweets:")
            #for follower_tweet in users.followers_tweets:
                #print(follower_tweet["text"])
                #time.sleep(1)

            # get the rossana and goran tweets
            ghAndRd = ["goranhagglund", "rossa_d"]
            ghAndRdTweets = []
            for id in ghAndRd:
                twythonaccess.check_if_requests_are_maximum(170)
                this_users_tweets = twythonaccess.authorize().get_user_timeline(screen_name=id, trim_user=True, include_rts=False)
                ghAndRdTweets.extend(this_users_tweets)

            # update the markov
            markov.update_markov(users.followers_tweets + ghAndRdTweets + users.followfollowers_tweets)
            print("markov updated")

        except Exception as exception:
            # print out the exception, and then sleep for 1 hour
            # the exception may be a rate limit, or it may be due to twitter's servers being down
            # either way, a sleep will help
            print(exception)
            print("will sleep for 1 hour to avoid exception")
            time.sleep(60*60)
            print("finished exception sleep; will resume tweet generation loop as normal")




# if called directly (as in "python3 mainbot.py"), then call main() function
if __name__ == "__main__":
    main()
