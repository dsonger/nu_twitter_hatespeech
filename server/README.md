# Server

The server will run continuously waiting for requests.

Requests are expected to use POST method, with parameters with the format: 

```
{tweet_id: TWEET_ID}
```

Where TWEET_ID is a string of the tweet id, according to the tweet URL.

## Requirements:
* Python 3.6.*
* Keras 
* Tensorflow or Theano
* Gensim
* Numpy
* Gevent
* Twython

## How to run locally:
Open the terminal and run the following command. Optional arguments in [].

```
server.py [-p PORT_NUMBER] -k TWITTER_APP_KEY -t TWITTER_APP_SECRET [-s]
```

### Argument details:

```
-p --port-number PORT_NUMBER :
	Port number to be used, by default uses 8080

-s --serve-page : 
	By default returns "403 Forbidden" on GET methods. 
	If this is argument is set, will serve a simple html 
	page to interact with server.
	
-k --app_key TWITTER_APP_KEY:

-t --app_secret TWITTER_APP_SECRET:
	
```