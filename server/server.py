import sys
import socket
import argparse
import functools

from urllib.parse import parse_qs
from gevent.pywsgi import WSGIServer
from lstm_classifier import TwitterHateClassifier
from twython import Twython
from twython.exceptions import TwythonError

DEFAULT_PORT_NUMBER = 8080

def error_response(start_response, status_code):
    start_response(status_code, [("Content-Type", "text/html; charset=utf-8")])
    return [bytes('<h1>%s</h1>' % status_code, "utf-8")]

def get_twitter_crawler(app_key, app_secret):
    app_key = 'inAzbLHc9OGYy2TJAyzvv8kVy'
    app_secret = 'XWv544eJo1IFdQZvNrEazM6tknDCJnsHxprlLsC1vEH3iKMEnX'

    twitter = Twython(app_key, app_secret, oauth_version=2)
    access_token = twitter.obtain_access_token()
    return Twython(app_key, access_token=access_token)
    
def application(env, start_response, classifier = None, serve_page = False, 
        response_page = None, tweet_crawler = None):
    print("env = ", env)

    # the JS uses POST, so if it isn't POST, either return default page or 403 status.
    if env["REQUEST_METHOD"] != "POST":
        if serve_page:
            start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
            return [response_page]
        else:
            return error_response(start_response, "403 Forbidden")
    
    # Try to get tweet data from Twitter API using requested tweet id.
    try:
        post_data = env["wsgi.input"].read().decode("utf-8")
        print(post_data)
        parsed = parse_qs(post_data)
        print(parsed)
        tweet_id = parsed["tweet_id"][0]
        print(tweet_id)
        tweet_data = tweet_crawler.show_status(id = tweet_id)        
        print(tweet_data)
    except TwythonError as err:
        print(err)
        if "429 (Too Many Requests)" in str(err):
            return error_response(start_response, "429 Too Many Requests")
        else:
            return error_response(start_response, "404 Not Found")
    except err:
        print(err)
        return error_response(start_response, "400 Bad Request")

    prediction = classifier.predict(tweet_data)
    response = '{"prediction": "%s"}' % prediction
    if not prediction == "none":
        # TODO: Generate URL from IBM NLU API
        news_url = "http://news.google.com"
        response = '{"prediction": "%s", "news_url": "%s"}' % (prediction, news_url)

    print("\ntweet:\n", tweet_data)
    print("\nresponse = ", response)

    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    return [bytes(response, "utf-8")]

def run_server():
    # Parse arguments.
    parser = argparse.ArgumentParser(description='Server for running Twitter hate speech detection.')
    parser.add_argument('-p', '--port-number', default=DEFAULT_PORT_NUMBER)
    parser.add_argument('-k', '--app-key', required=True)
    parser.add_argument('-t', '--app-secret', required=True)
    parser.add_argument('-s', '--serve-page', action='store_true', default=False)
    args = parser.parse_args()
    
    port_number = int(args.port_number)
    app_key = args.app_key
    app_secret = args.app_secret
    serve_page = args.serve_page
    response_page = None
    
    # Load classifier.
    classifier = TwitterHateClassifier()
    
    # Start Twython twitter crawler.
    tweet_crawler = get_twitter_crawler(app_key, app_secret)
    
    # Load interactive response page.
    if serve_page:
        with open('client.html', 'rb') as file:
            response_page = file.read()
            print("** RESPONSE PAGE: **\n")
            print(response_page)
    
    # Start server
    host = socket.gethostbyname(socket.gethostname())
    address = host, port_number
    app = functools.partial(application, classifier = classifier, serve_page = serve_page, response_page = response_page, tweet_crawler = tweet_crawler)
    server = WSGIServer(address, app)
    server.backlog = 256
    print('\n########################################\n')
    print('Serving on http://%s:%s' % (host, port_number))
    print('Press ctrl-C or cmd-C to stop.')
    print('\n########################################\n')
    server.serve_forever()

if __name__ == "__main__":
    run_server()