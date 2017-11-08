import sys
import socket
import argparse
import functools

from urllib.parse import parse_qs
from gevent.pywsgi import WSGIServer
from lstm_classifier import TwitterHateClassifier

DEFAULT_PORT_NUMBER = 8080

def application(env, start_response, classifier = None, serve_page = False, response_page = None):
    print("env = ", env)

    # the JS uses POST, so if it isn't POST, either return default page or 403 status.
    if env["REQUEST_METHOD"] != "POST":
        if serve_page:
            start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
            return [response_page]
        else:
            start_response("403 Forbidden", [("Content-Type", "text/html; charset=utf-8")])
            return [b'<h1>403 Forbidden</h1>']

    post_data = env["wsgi.input"].read().decode("utf-8")
    
    # TODO: check if post data contains valid tweet id
    if post_data is None:
        start_response("400 Bad Request", [("Content-Type", "text/html; charset=utf-8")])
        return [b'<h1>400 Bad Request</h1>']
    
    parsed = parse_qs(post_data)
    # tweet_id = parsed["tweetid"]
    tweet_text = parsed["tweet"][0]
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    prediction = classifier.predict({"text": tweet_text})
    print("\ntweet text:\n", tweet_text)
    print("\nprediction = ", prediction)
    response = bytes('{"prediction": "%s"}' % prediction, "utf-8")
    return [response]

def run_server():
    # Parse arguments.
    parser = argparse.ArgumentParser(description='Server for running Twitter hate speech detection.')
    parser.add_argument('-p', '--port-number', default=DEFAULT_PORT_NUMBER)
    parser.add_argument('-s', '--serve-page', action='store_true', default=False)
    args = parser.parse_args()
    port_number = int(args.port_number)
    serve_page = args.serve_page
    response_page = None
    
    # Load classifier.
    classifier = TwitterHateClassifier()
    
    # Load interactive response page.
    if serve_page:
        with open('client.html', 'rb') as file:
            response_page = file.read()
            print("** RESPONSE PAGE: **\n")
            print(response_page)
    
    # Start server
    host = socket.gethostbyname(socket.gethostname())
    address = host, port_number
    app = functools.partial(application, classifier = classifier, serve_page = serve_page, response_page = response_page)
    server = WSGIServer(address, app)
    server.backlog = 256
    print('\n########################################\n')
    print('Serving on http://%s:%s' % (host, port_number))
    print('Press ctrl-C or cmd-C to stop.')
    print('\n########################################\n')
    server.serve_forever()

if __name__ == "__main__":
    run_server()