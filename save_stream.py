from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from decouple import config
import time

# Variables that contains the user credentials to access Twitter API
access_token = config('access_token_key')
access_token_secret = config('access_token_secret')
consumer_key = config('consumer_key')
consumer_secret = config('consumer_secret')


# This is a basic listener, save in JSON for date
class StdOutListener(StreamListener):

    def __init__(self, fprefix = 'streamer'):
        self.counter = 0
        self.fprefix = fprefix
        self.output  = open('data/' + fprefix + '.' 
                            + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
        self.delout  = open('delete.txt', 'a')

    def on_data(self, data):

        self.output.write(data + "\n")
        self.counter += 1
        #Change number for limit         
        if self.counter >= 20000:
            self.output.close()
            self.output = open('data/' + self.fprefix + '.' 
                               + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
            self.counter = 0
        return True

    def on_error(self, status):
        print (status)


if __name__ == '__main__':

    # This handles Twitter authetification and the connection to Twitter Streaming API.
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # This line filter Twitter Streams to capture data by the name in track
    stream.filter(track=['python', 'java'])
