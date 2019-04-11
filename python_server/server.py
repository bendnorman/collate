from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler, test
from urllib.parse import urlparse
from urllib.parse import unquote
import json

from io import BytesIO

from collate import Collate


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
        
        # Get and Post long, lat
        address = unquote(urlparse(self.path).query.split('=')[1])
        print(f"Address: {address}")
        
        data = cl.address_data_request(address)
        print(data)
        
        self.wfile.write(str.encode(json.dumps(data)))
    
    
try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), CORSHTTPRequestHandler)
    print(f'Started httpserver on port {PORT_NUMBER}')

    cl = Collate()

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print(f'^C received, shutting down the web server')
    server.socket.close()
