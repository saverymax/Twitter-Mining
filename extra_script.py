import SocketServer
import SimpleHTTPServer

import requests
import multiprocessing

def open_server():


    # Variables
    PORT = 8888
    URL = 'localhost:{port}'.format(port=PORT)

    # Setup simple sever
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print("Serving at port", PORT)

    # start the server as a separate process
    server_process = multiprocessing.Process(target=httpd.serve_forever)
    server_process.daemon = True
    server_process.start()

open_server()
