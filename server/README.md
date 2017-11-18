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
* IBM Watson Developer Cloud

## How to run locally:
Open the terminal and run the following command.

```
server.py [-p PORT_NUMBER] [-s] --twitter-key TWITTER_APP_KEY --twitter-secret TWITTER_APP_SECRET --ibm-username IBM_APP_USERNAME --ibm-password IBM_APP_PASSWORD
```

Note: Optional arguments in [] and argument values are in upper-case.

### Argument details:

```
-p --port-number PORT_NUMBER :
	Port number to be used, by default uses 8080

-s --serve-page :
	By default returns "403 Forbidden" on GET methods. 
	If this is argument is set, will serve a simple html 
	page to interact with server.
	
--twitter-key TWITTER_APP_KEY:
	The key credentials given by the Twitter app.
	
--twitter-secret TWITTER_APP_SECRET:
	The secret credentials given by the Twitter app.
	
--ibm-username IBM_APP_USERNAME:
	The username credentials used by IBM NLU API.

--ibm-password IBM_APP_PASSWORD:
	The password credentials used by IBM NLU API.
```