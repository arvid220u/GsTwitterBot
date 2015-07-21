# import re, to parse the string
import re
# import randint
from random import randint
# import the twython api, for not sending the same tweet twice
import twythonaccess
# import time for testing
import time

class Markov:

    # The tweet list, which contins not just text, but also
    # other data, e.g. an image url (if there's an img included)
    tweet_list = []
    # an array of the tweets text
    tweets_text = []
    # the markov dictionary. For every two words, there will be an
    # array of associated words which naturally come next.
    markov_dictionary = {}
    # a list of the two words which have begun tweets
    beginning_words = []
    beginning_words_full_tweets = {}

    # The initializer, which takes a list of tweets as an argument
    def __init__(self, tweet_list):
        self.tweet_list = tweet_list
        self.tweets_text = self.strings_from_tweets(tweet_list)
        self.markov_dictionary = self.markov_dictionary_from_strings(self.tweets_text)

    # the update function is the same as the init
    def update_markov(self, tweet_list):
        self.tweet_list = tweet_list
        self.tweets_text = self.strings_from_tweets(tweet_list)
        self.markov_dictionary = self.markov_dictionary_from_strings(self.tweets_text)

    # Generate an array of strings, stripped of http links,
    # from an array of tweets
    def strings_from_tweets(self, tweets):
        strings = []
        print("parsing tweets")
        # loop through each tweet
        for tweet in tweets:
            tweet_text = tweet["text"]
            # remove any urls
            tweet_text = re.sub(r'(http)\S+(t.co)\S+', '', tweet_text)
            # remove all usernames
            tweet_text = re.sub(r'@\S+', '', tweet_text)
            # only append to strings if the length is greater than zero
            if len(tweet_text.split()) > 0:
                tweet["text"] = tweet_text
                strings.append(tweet)
            else:
                print("no words in tweet: " + tweet["text"])
        # return the list
        return strings

    # this function will generate the dictionary used in the
    # markov algorithm. The dictionary's keys consist of every
    # word, which has any word after it. The values are an
    # array of the words which appears after the word.
    # there can be many instances of a particular word in
    # the same value array, as that signifies that that
    # word is more common.
    def markov_dictionary_from_strings(self, strings):
        dictionary = {}
        # this array is used for tracking if a certain tweet has aready been parsed
        # if so, that tweet should add its beginning_words again, but not in markov_dict
        parsed_tweets = []
        print("setting up markov dictionary")
        for string in strings:
            # the text
            text = string["text"]
            # get an array of all the words in the string
            words = text.split()
            # only add tweet words to beginning_words if lang is sv
            if string["lang"] == "sv": #no more: this excluded many swedish tweets
                # if number of words is less than two, then add it to the beginning
                # words, and continue loop
                if len(words) < 2:
                    self.beginning_words.append(words[0])
                    self.beginning_words_full_tweets[words[0]] = text
                    continue
                # add the first and second word to the beginning words
                self.beginning_words.append(words[0] + " " + words[1])
                self.beginning_words_full_tweets[words[0] + " " + words[1]] = text

            # If number of words is less than two, continue loop
            if len(words) < 2:
                continue

            # if tweet has already been parsed, end execution here
            if string in parsed_tweets:
                #time.sleep(1)
                print("following tweet already parsed: " + text)
                continue
            # the last_word and last_last_word variables will be used as the key
            # for the next word
            # they should always be lowercase
            last_last_word = words[0].lower()
            last_word = words[1].lower()
            del words[0]
            del words[0]
            # iterate over the words, and add them as values
            # to the dictionary, with the last_word and last_last_word as key
            for word in words:
                # first check if key is already present
                if last_last_word + last_word in dictionary:
                    # only append to the array of words
                    dictionary[last_last_word + last_word].append(word)
                    # sleep so these can be read
                    #time.sleep(1)
                    print("good markov")
                    #print("good words: " + last_last_word + ", " + last_word)
                    #print("following words for the good words:")
                    #print(dictionary[last_last_word + last_word])
                    #time.sleep(4)
                else:
                    # create a list, so other words can
                    # use the same key
                    dictionary[last_last_word + last_word] = [word]
                    #time.sleep(1)
                    print("bad")
                # now update last_word and last_last_word
                last_last_word = last_word
                last_word = word.lower()
            # add to parsed_tweets
            parsed_tweets.append(string)

        # return the dictionary
        print("finished creating markov dictionary")
        return dictionary




    # this function will generate a tweet, based on the
    # markov dictionary. It will start with a word from
    # the beginnning_words list, and then use the dictionary
    # to get a second word, etc. It will stop when the word
    # retrieved, isn't found as a key in the dictionary.
    def generate_tweet(self):
        # the tweet which will be returned
        tweet = ""
        # if the tweet is over 140 characters, then a
        # new tweet will be generated
        tweet_length = 141
        # if the tweet is the same as another from self
        tweet_has_already_been_sent = False
        while tweet_length > 140 or tweet_has_already_been_sent:
            tweet_has_already_been_sent = False
            #print("running loop again because tweet has been sent: ")
            #print(tweet_has_already_been_sent)
            #print("or because tweet length is over 140:")
            #print(tweet_length > 140)
            # get a random number, which can be used as an index
            beginning_word_index = randint(1,len(self.beginning_words)) - 1
            random_beginning_word = self.beginning_words[beginning_word_index]
            tweet = random_beginning_word
            beginning_word_tweet = self.beginning_words_full_tweets[random_beginning_word]
            beginning_word_tweet_words = beginning_word_tweet.split()
            # the last_word and last_last_word will be used access the next word
            last_words = random_beginning_word.split()
            last_last_word = last_words[0].lower()
            last_word = ""
            if len(last_words) > 1:
                last_word = last_words[1].lower()
            # add words to the tweet, while last_word + last_last_word exists in
            # markov_dictionary
            # prevent an endless loopby setting the maximum number of cycles to 140. This means the tweet will get 142 words long by maximum, which by fact is over 140 characters.
            maximum_cycles = 140
            current_cycle = 1
            while last_last_word + last_word in self.markov_dictionary and current_cycle < maximum_cycles:
                # get a random word which corresponds to the key
                possible_next_words = self.markov_dictionary[last_last_word + last_word]
                random_index = randint(1, len(possible_next_words)) - 1
                print("maybe index: " + str(random_index))
                if len(possible_next_words) > 1:
                    for index, possible_word in enumerate(possible_next_words):
                        print("possible word: " + possible_word)
                        if possible_word in beginning_word_tweet_words and index == random_index:
                            # new random index (is not same)
                            print("new index")
                            while random_index == index:
                                random_index = randint(1, len(possible_next_words)) - 1
                #random_index = randint(1, len(possible_next_words)) - 1
                next_word = possible_next_words[random_index]
                print("Available words: " + str(len(possible_next_words)))
                print("Chose #" + str(random_index) + " " + next_word)
                # add next_word to the tweet
                tweet = tweet + " " + next_word
                # last_word becomes last_last_word
                last_last_word = last_word
                # next_word becomes last_word
                last_word = next_word.lower()
                # update the current_cycle
                current_cycle += 1

            # 1/75 of all tweets shuld have all letters uppercase
            if randint(1, 75) == 2:
                tweet = tweet.upper()
                if len(tweet) > 110:
                    tweet_words = tweet.split()
                    tweet = ""
                    for tweet_word in tweet_words:
                        if randint(1,3) == 2:
                            tweet_word = tweet_word.lower()
                        tweet = tweet + tweet_word
            # check if nothing has been changed in the tweet
            if tweet == beginning_word_tweet:
                # run the loop again
                tweet_has_already_been_sent = True
                print("Nothing changed in tweet: " + tweet)
                time.sleep(4)
                continue
            # always add #gs to the tweet
            tweet = tweet + " #gs"
            print("tweet proposition: " + tweet)
            # the tweet is generated, now update the length, so
            # it isn't longer than 140
            tweet_length = len(tweet)
            print("tweet of length: ")
            print(tweet_length)
            #time.sleep(4)
            # check if this tweet already has been sent            twythonaccess.check_if_requests_are_maximum()
            twythonaccess.check_if_requests_are_maximum(170)
            api = twythonaccess.authorize()
            # get all tweets from me
            all_tweets_from_me = api.get_user_timeline(screen_name=twythonaccess.screen_name, trim_user = True, include_rts = False, count = 200)
            while len(all_tweets_from_me) > 0:
                for tweet_from_me in all_tweets_from_me:
                    if tweet_from_me["text"] == tweet:
                        # this tweet has already been sent
                        tweet_has_already_been_sent = True
                        print("already sent: " + tweet)
                    else:
                        # if tweet only have less than 3 words not in common,
                        # don't send it
                        original_tweet_words = tweet_from_me["text"].split()
                        new_tweet_words = tweet.split()
                        full_length = len(new_tweet_words)
                        common_words = 0
                        for index, word in enumerate(new_tweet_words):
                            if index < len(original_tweet_words):
                                if word == original_tweet_words[index]:
                                    common_words += 1
                        if common_words == full_length:
                            tweet_has_aleady_been_sent = True
                            print("already sent (almost): " + tweet)
                # get new all tweets, as previous may not have been all
                twythonaccess.check_if_requests_are_maximum(170)
                api = twythonaccess.authorize()
                all_tweets_from_me = api.get_user_timeline(screen_name=twythonaccess.screen_name, trim_user=True, include_rts=False, count=200, max_id=all_tweets_from_me[len(all_tweets_from_me)-1]["id"]-1)


        # the tweet has been generated, and is 140 characters
        # or less. Now, if tweet is shorter than 25
        # characters, add 'Gott snack: ' before it.
        if tweet_length < 25:
            tweet = "Gott snack: " + tweet

        # now tweet is generated
        print("tweet approved: " + tweet)
        # return it
        return tweet




    # This method takes a beginning word and generates a tweet from it
    def generate_tweet_with_beginning_word(self, chosen_beginning_words):
        # the tweet which will be returned
        tweet = ""
        # if the tweet is over 140 characters, then a
        # new tweet will be generated
        tweet_length = 141
        # if the tweet is the same as another from self
        tweet_has_already_been_sent = False
        #while tweet_length > 140 or tweet_has_already_been_sent:
        # init with the chosen word
        tweet = chosen_beginning_words
        beginning_word_tweet = self.beginning_words_full_tweets[chosen_beginning_words]
        beginning_word_tweet_words = beginning_word_tweet.split()
        # the last_word and last_last_word will be used access the next word
        last_words = chosen_beginning_words.split()
        last_last_word = last_words[0].lower()
        last_word = ""
        if len(last_words) > 1:
            last_word = last_words[1].lower()
        # add words to the tweet, while last_word + last_last_word exists in
        # markov_dictionary
        while last_last_word + last_word in self.markov_dictionary:
            # get a random word which corresponds to the key
            possible_next_words = self.markov_dictionary[last_last_word + last_word]
            random_index = randint(1, len(possible_next_words)) - 1
            print("maybe index: " + str(random_index))
            if len(possible_next_words) > 1:
                for index, possible_word in enumerate(possible_next_words):
                    print("possible word: " + possible_word)
                    if possible_word in beginning_word_tweet_words and index == random_index:
                        # new random index (may be same)
                        print("new index")
                        while random_index == index:
                            random_index = randint(1, len(possible_next_words)) - 1
            next_word = possible_next_words[random_index]
            print("Available words: " + str(len(possible_next_words)))
            print("Chose #" + str(random_index) + " " + next_word)
            # add next_word to the tweet
            tweet = tweet + " " + next_word
            # last_word becomes last_last_word
            last_last_word = last_word
            # next_word becomes last_word
            last_word = next_word.lower()
        # 1/75 of all tweets shuld have all letters uppercase
        if randint(1, 75) == 2:
            tweet = tweet.upper()
            if len(tweet) > 110:
                tweet_words = tweet.split()
                tweet = ""
                for tweet_word in tweet_words:
                    if randint(1,3) == 2:
                        tweet_word = tweet_word.lower()
                    tweet = tweet + tweet_word
        # check if nothing has been changed in the tweet
        if tweet == beginning_word_tweet:
            # run the loop again
            tweet_has_already_been_sent = True
            print("Nothing changed in tweet: " + tweet)
        # always add #gs to the tweet
        tweet = tweet + " #gs"
        print("tweet proposition: " + tweet)
        # the tweet is generated, now update the length, so
        # it isn't longer than 140
        tweet_length = len(tweet)
        # check if this tweet already has been sent            twythonaccess.check_if_requests_are_maximum()
        twythonaccess.check_if_requests_are_maximum(170)
        api = twythonaccess.authorize()
        # get all tweets from me
        all_tweets_from_me = api.get_user_timeline(screen_name=twythonaccess.screen_name, trim_user = True, include_rts = False, count = 200)
        while len(all_tweets_from_me) > 0:
            for tweet_from_me in all_tweets_from_me:
                if tweet_from_me["text"] == tweet:
                    # this tweet has already been sent
                    tweet_has_already_been_sent = True
                    print("already sent: " + tweet)
            # update the a tweets frm me t account for new tweets
            twythonaccess.check_if_requests_are_maximum(170)
            api = twythonaccess.authorize()
            all_tweets_from_me = api.get_user_timeline(screen_name=twythonaccess.screen_name, trim_user=True, include_rts=True, count=200, max_id=all_tweets_from_me[len(all_tweets_from_me)-1]["id"]-1)

        # the tweet has been generated. Now, if tweet is shorter than 25
        # characters, add 'Gott snack: ' before it (in some cases).
        if tweet_length < 25 and randint(1,4) == 2:
            tweet = "Gott snack: " + tweet

        # now tweet is generated, if nuber of characters is not over 140 and the tweet is not in
        if tweet_length < 140 and not tweet_has_already_been_sent:
            print("tweet approved: " + tweet)
            # return it
            return tweet
        else:
            return None
    
    
    # This function generates a reply to the tweet specified
    def generate_reply(to_tweet):
        while True:
            original_tweet_id = to_tweet["id"]
            original_tweet_text = to_tweet["text"].encode(encoding='UTF-8')
            original_tweet_userid = to_tweet["user"]["id"]
            # get the screen name
            twythonaccess.check_if_requests_are_maximum(170)
            original_tweet_screenname = twythonaccess.authorize().show_user(user_id=original_tweet_userid)["screen_name"].encode(encoding='UTF-8')
            
            # 75%, the bot will reply with a markov-generated
            # tweet, by first searching for a word from the tweet in markov's startwords.
            # 12.5% it will reply with a variation of
            # gs. 12.5% it will reply by citing a word and
            # writing gs next to it.
            reply_tweet = ''
            random = randint(1,8)
            if random == 1:
                # cite word
                original_tweet_words = original_tweet_text.split()
                random_word_index = randint(1, len(original_tweet_words)) - 1
                random_word = original_tweet_words[random_word_index]
                randomm = randint(1,3)
                if randomm == 1:
                    reply_tweet = '"' + random_word + '". gs'
                elif randomm == 2:
                    reply_tweet = 'Gott snack: "' + random_word + '"'
                elif randomm == 3:
                    reply_tweet = '"' + random_word + '" ...gs'
            elif random > 2:
                # generate a tweet with a word from the original tweet
                original_tweet_words = original_tweet_text.lower().split()
                # this str contains the currently best beginning_words
                best_beginning_words = ""
                # the ranking is based on where the word match is found
                # the earlier the better, because then there is a higher chance of the actual word showing up in the actual tweet
                # set to dummy value of 100
                match_index = 100
                # loop over each key and value in beginning_words_full_tweets
                for beginning_words, full_tweet in self.beginning_words_full_tweets.iteritems():
                    # create a list from a lowercase version of the tweet
                    tweet_words = full_tweet.lower().split()
                    for index, word in enumerate(tweet_words):
                        if word in original_tweet_words:
                            # match is found, at index index
                            # check if index is lower than match_index
                            if index < match_index:
                                best_beginning_words = beginning_words
                                match_index = index
                                # if index is zero or one,
                                # there is no need to search anyore
                                # therefore, break the loop
                                if index < 2:
                                    break
                    else:
                        # this is executed if the loop of the words
                        # terminated normally, i.e. not with break
                        continue
                    # will break if index is below 2
                    break
                tweet_from_word = False
                if best_beginning_words is not "":
                    reply_tweet = self.generate_tweet_with_beginning_word(best_beginning_words)
                    if reply_tweet is not None:
                        tweet_from_word = True
                if not tweet_from_word:
                    # genereate a random markov tweet
                    reply_tweet = self.generate_tweet()
            elif random == 2:
                randomm = randint(1,3)
                if randomm == 1:
                    reply_tweet = "Ganska gs."
                elif randomm == 2:
                    reply_tweet = "gs"
                elif randomm == 3:
                    reply_tweet = "Gott snack."
                    
            # add @username at the beginning, and send the tweet
            reply_tweet = "@" + original_tweet_screenname + " " + reply_tweet
            print("about to tweet: " + reply_tweet)
            if len(reply_tweet) <= 140:
                if twythonaccess.send_tweet(tweet=reply_tweet, in_reply_to_status_id=original_tweet_id):
                    break
