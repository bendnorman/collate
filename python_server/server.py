from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler, test
from urllib.parse import urlparse

from io import BytesIO

import collate


PORT_NUMBER = 8080

# This class will handles any incoming request from
# the browser

class CORSHTTPRequestHandler(SimpleHTTPRequestHandler):

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super(CORSHTTPRequestHandler, self).end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        address = urlparse(self.path).query.split('=')[1]
        print(address)
        
        response = BytesIO()
        response.write(b'This is POST request. ')
        print(response.getvalue())
        self.wfile.write(response.getvalue())
    
    
try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), CORSHTTPRequestHandler)
    print(f'Started httpserver on port {PORT_NUMBER}')
    
    print(collate.plot_realestate_trends('1 East Loop Rd.'))


    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print(f'^C received, shutting down the web server')
    server.socket.close()
