# Import the twython module
import twythonaccess
# import time and sys
import time
# import the users class
from users import Users
# import markov
from markov import Markov

# temp sleep
#time.sleep(60*60*11)


# Declare all the global variabes which will be used

# The users object will contain
# the two arrays: followers and followfollowers
# This instantiation will also start the process of checking for new followers,
# and in those cases greet them
users = Users()
print "initialized users"
# instantiate the markov object
#markov = Markov(users.followers_tweets + users.followfollowers_tweets)

# do this instead: mix the followers' tweets with tweets from goranhagglund and rossa_d
ghAndRd = ["goranhagglund", "rossa_d"]
ghAndRdTweets = []
for screen_name in ghAndRd:
    twythonaccess.check_if_requests_are_maximum(170)
    this_users_tweets = twythonaccess.authorize().get_user_timeline(screen_name=screen_name, trim_user=True, include_rts=False)
    ghAndRdTweets.extend(this_users_tweets)
    print "a tweet from " + screen_name + ": " + this_users_tweets[0]["text"]
    time.sleep(5)

markov = Markov(users.followers_tweets + ghAndRdTweets + users.followfollowers_tweets)
print "initialized markov"

# the user shoud be able to reference the markov object
users.markov = markov


print "setup complete"

# the run loop, which in the future will continue in infinity
while True:
    print "start loop"

    # get a tweet
    #tweet = markov.generate_tweet()
    
    # send tweet
    while True:
        # generate new tweet
        tweet = markov.generate_tweet()
	print "tweet generated: " + tweet
        if twythonaccess.send_tweet(tweet):
            # the generated tweet is okay
            print "tweet approved or passed"
            break

    # sleeping point, if need for sleep
    # sleep for one day
    # will be a total delay between tweets at around 24.1 hours, which is good
    # Decrease this sleep amout as new followers are gathered
    print "will sleep for 25 hours"
    time.sleep(60 * 60 * 25)
    print "has slept for 25 hours"
    # TEMPORARILY DISABLED

    # update the users followers
    users.check_new_followers()
    print "updated followers"

    #print "followers:"
    #for follower in users.followers:
        #print follower["screen_name"]
        #time.sleep(1)
    #print "followfollowers:"
    #for followfollower in users.followfollowers:
        #print followfollower["screen_name"]
        #time.sleep(1)
    
    # update the tweets
    users.check_new_tweets()
    print "updated tweets"

    #print "follower's tweets:"
    #for follower_tweet in users.followers_tweets:
        #print follower_tweet["text"]
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
    print "markov updated"
