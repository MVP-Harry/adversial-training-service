from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import torch

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # Gets the size of data
        post_data = self.rfile.read(content_length) # Gets the data itself
        try:
            data = json.loads(post_data.decode('utf-8'))
            number = data.get('number')
            
            # Check if 'number' is a valid integer
            if isinstance(number, int):
                response_dict = {'number': number + 1}
                response_json = json.dumps(response_dict)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(response_json.encode('utf-8'))
            else:
                self.send_error(400, "Invalid input. Please send a JSON with an integer 'number'.")
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON format. Please send a valid JSON.")

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, addr="localhost", port=8080):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting http server on {addr}:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()