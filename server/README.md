# Server

## Requirements:
* Python 3.6.*
* Keras 
* Tensorflow or Theano
* Gensim
* Numpy
* Gevent

## How to run locally:
Open the terminal and run the following command. This will bring up the server with the default options.

```
python server.py
```

## Usage:

```
server.py [-p PORT_NUMBER] [-s]
```

optional arguments:

```
-p --port-number : Port number to be used, by default uses 8080
-s --serve-page	PORT_NUMBER : By default returns "403 Forbidden" on GET
	methods.  If this is argument is set, will
	serve a simple html  page to interact with
	server.
```