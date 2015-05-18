# This module provides the api twython object, which is used to access the api

# import time, to enable the sleep function
import time

# Import twython
from twython import Twython

# import the api keys
import apikeys


# Get all the keys for the GsMarkovReplier app on the GsGottsnack account
#CONSUMER_KEY = '8MrS7nG1eG33Lt1jZXZUgYHfn'#'b6Fh8O3ZiWH8NGgVQcFspUNKw8MrS7nG1eG33Lt1jZXZUgYHfn'
#CONSUMER_SECRET = 'F25sNhnyjD9vIjyYz1hFk0YuLwX2ZKvN0qQmuijjpXqqrUdJqI'#'TZAtcy5PkK0Sm0lWYhnrdQbIfmP90HOvi6ZqaHZRaY5oqeUz9K'
#ACCESS_TOKEN= '2730134586-JWMzTfPCGoTt8YxK96yYbQ8livtmrHpXXaylJTS'#'2730134586-BswBNnx0X4uVYZJTp81GpIV5v6ETX07TKz2ZSmu'
#ACCESS_TOKEN_SECRET = 'cLfLccU5qd1rsTA0oq8LBCG1NmBdafiUZHV7RTLlBjQNL'#'SYxQXehlAMKruamriEpfdJEgJeXehsbrIvslJYGDgm70acTlwW3hkb0l6Fdm8fWy5kkTomJxv0s50WS1vy0rgily7e'

# The api variable is the way to access the api
def authorize():
    return Twython(apikeys.CONSUMER_KEY, apikeys.CONSUMER_SECRET, apikeys.ACCESS_TOKEN, apikeys.ACCESS_TOKEN_SECRET)

# the screen name for self
screen_name = "gsgottsnack"

# this method sends a tweet, by first checking with me
def send_tweet(tweet, in_reply_to_status_id=0):
    global screen_name
    # send the tweet first as a dm to arvid220u
    # if he replies with yes, send the tweet.
    # if he replies with no, don't send the tweet (generate a new one)
    # if he replies with pass, don't sendd the tweet and don't generate a new one
    
    # get the most recent dm sent to me. the answer should be newer.
    check_if_requests_are_maximum(13)
    previous_reply_id = authorize().get_direct_messages(include_entities=False)[0]["id"]

    # send the dm to arvid with the tweet
    check_if_requests_are_maximum(13)
    authorize().send_direct_message(screen_name="ArVID220u", text=tweet)
    print "tweet in review: " + tweet
    arvid_has_approved_or_aborted = False
    while not arvid_has_approved_or_aborted:
        check_if_requests_are_maximum(13)
        # get the dms more recent than the previous reply
        all_dms = authorize().get_direct_messages(include_entities=False, since_id=previous_reply_id)
        response_since_gs_message = ""
        # get the last reply, make sure it's in the right conversation
	# the last reaply is at index 0
        # if all_dms length is greater than 0
        if len(all_dms) > 0:
            last_message_index = 0
            last_message = all_dms[last_message_index]
            last_message_is_arvid = False
            while not last_message_is_arvid:
                if last_message["sender_screen_name"] == "ArVID220u":
                    response_since_gs_message = last_message["text"]
                    last_message_is_arvid = True
                else:
                    last_message_index += 1
                    last_message = all_dms[last_message_index]
            print "last message: " + last_message["text"]
            if last_message_is_arvid:
                print "arvid's reponse: " + response_since_gs_message
                if response_since_gs_message == "Yes":
                    # send the tweet
                    check_if_requests_are_maximum(13)
                    if in_reply_to_status_id == 0:
                        authorize().update_status(status=tweet)
                    else:
                        authorize().update_status(status=tweet, in_reply_to_status_id=in_reply_to_status_id)
                    print "sent tweet: " + tweet
                    arvid_has_approved_or_aborted = True
                if response_since_gs_message == "Pass":
                    arvid_has_approved_or_aborted = True
                elif response_since_gs_message == "No":
                    # return false, which will make this function be called again, with a new tweet (hopefully)
                    return False
        if not arvid_has_approved_or_aborted:
            time.sleep(60*6)

    # return true, meaning this function should not be called again
    return True

# Store number of requests, so that they won't exceed 14
requests_since_last_sleep = 0
# This method is called everytime a request is to be made
# IF the requests variable is over limit, then it sleeps for 17 minutes
# if the requests variable isn't over limit, then increment it by one
def check_if_requests_are_maximum(limit):
    global requests_since_last_sleep
    print "Requests since last sleep: " + str(requests_since_last_sleep)
    if requests_since_last_sleep >= limit:
        print "will sleep"
        time.sleep(17*60)
        print "has slept"
        # reset requests
        requests_since_last_sleep = 0
    # increment requests
    requests_since_last_sleep += 1

