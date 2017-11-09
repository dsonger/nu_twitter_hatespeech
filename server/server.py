import sys
import socket
import argparse
import functools
import json

from urllib.parse import parse_qs
from gevent.pywsgi import WSGIServer
from lstm_classifier import TwitterHateClassifier
from twython import Twython
from twython.exceptions import TwythonError
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as Features

DEFAULT_PORT_NUMBER = 8080

def error_response(start_response, status_code):
    start_response(status_code, [("Content-Type", "text/html; charset=utf-8")])
    return [bytes('<h1>%s</h1>' % status_code, "utf-8")]

def get_twitter_api(app_key, app_secret):
    app_key = 'inAzbLHc9OGYy2TJAyzvv8kVy'
    app_secret = 'XWv544eJo1IFdQZvNrEazM6tknDCJnsHxprlLsC1vEH3iKMEnX'

    twitter = Twython(app_key, app_secret, oauth_version=2)
    access_token = twitter.obtain_access_token()
    return Twython(app_key, access_token=access_token)
    
def get_ibm_api(username, passsword):
    return NaturalLanguageUnderstandingV1(
        username="002e5382-7ca8-45fd-9cf3-7d31cba37479",
        password="2gNm8tNui0Kz",
        version="2017-02-27")

def create_news_url(ibm_api, tweet_text):
    response = ibm_api.analyze(
      text = tweet_text,
      features=[
        Features.Categories()
      ]
    )
    print(response)
    category_label = response["categories"][0]["label"]
    print(category_label)
    query = (" ".join(category_label.split("/")[1:])).replace(" ", "%20")
    print(query)
    news_url = "http://news.google.com/news/search/section/q/%s" % query
    print(news_url)
    return news_url
    
def application(env, start_response, classifier = None, serve_page = False, 
        response_page = None, tweet_api = None, ibm_api = None):
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
        parsed = parse_qs(post_data)
        tweet_id = parsed["tweet_id"][0]
        tweet_data = tweet_api.show_status(id = tweet_id)        
        print("tweet_data =", tweet_data)
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
        news_url = create_news_url(ibm_api, tweet_data["text"])
        response = '{"prediction": "%s", "news_url": "%s"}' % (prediction, news_url)

    print("\ntweet:\n", tweet_data)
    print("\nresponse = ", response)

    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    return [bytes(response, "utf-8")]

def run_server():
    # Parse arguments.
    parser = argparse.ArgumentParser(description='Server for running Twitter hate speech detection.')
    parser.add_argument('-p', '--port-number', default=DEFAULT_PORT_NUMBER)
    parser.add_argument('-s', '--serve-page', action='store_true', default=False)
    parser.add_argument('--twitter-key', required=True)
    parser.add_argument('--twitter-secret', required=True)
    parser.add_argument('--ibm-username', required=True)
    parser.add_argument('--ibm-password', required=True)
    args = parser.parse_args()
    
    port_number = int(args.port_number)
    serve_page = args.serve_page
    twitter_key = args.twitter_key
    twitter_secret = args.twitter_secret
    ibm_username = args.ibm_username
    ibm_password = args.ibm_password
    response_page = None
    
    # Load classifier.
    classifier = TwitterHateClassifier()
    
    # Start Twython twitter api.
    tweet_api = get_twitter_api(twitter_key, twitter_secret)
    
    # Start NaturalLanguageUnderstandingV1 IBM api.
    ibm_api = get_ibm_api(twitter_key, twitter_secret)
    
    # Load interactive response page.
    if serve_page:
        with open('client.html', 'rb') as file:
            response_page = file.read()
            print("** RESPONSE PAGE: **\n")
            print(response_page)
    
    # Start server
    host = socket.gethostbyname(socket.gethostname())
    address = host, port_number
    app = functools.partial(application, classifier = classifier, serve_page = serve_page, response_page = response_page, tweet_api = tweet_api, ibm_api = ibm_api)
    server = WSGIServer(address, app)
    server.backlog = 256
    print('\n########################################\n')
    print('Serving on http://%s:%s' % (host, port_number))
    print('Press ctrl-C or cmd-C to stop.')
    print('\n########################################\n')
    server.serve_forever()

if __name__ == "__main__":
    run_server()