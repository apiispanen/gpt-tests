"""
This script runs the SpinnrAIWebService application using a development server.
Look in SpinnrAIWebService\views.py for the actual code that runs the server.
"""

# import logging
# # from gevent.pywsgi import WSGIServer
# # from geventwebsocket.handler import WebSocketHandler

# # make filename a path above the current directory
# logging.basicConfig(filename='./output.log', level=logging.DEBUG)

from os import environ, getenv
from AIWebService import app
import dotenv
dotenv.load_dotenv()

if __name__ == '__main__':
    HOST = '0.0.0.0' 
    # HOST = 'localhost'
    """try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555"""

    # Use gevent's WSGIServer with WebSocketHandler for Flask-SocketIO
    # http_server = WSGIServer((HOST, PORT), app, handler_class=WebSocketHandler, 
    #                          keyfile=getenv('SSL_KEY'), certfile=getenv('SSL_CERT'))
    # http_server.serve_forever()
    # instead of the above, use the following:
    app.run(host=HOST, debug=False)
    # app.run(host=HOST, port=PORT, debug=False)