from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import torch
import pickle

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        self.send_error(400, "potatto")
        # content_length = int(self.headers['Content-Length']) # Gets the size of data
        # post_data = self.rfile.read(content_length) # Gets the data itself
        # try:
        #     data = pick.loads(post_data.decode('utf-8'))
        #     dataloader = data.get('dataloader')
        #     model = data.get('model')
        #     options = data.get('options')
        #     self.send_response(200)
        #     self.send_header('Content-type', 'application/pickle')
        #     self.end_headers()
        #     self.wfile.write(response_json.encode('utf-8'))
        #     # Check if 'number' is a valid integer
        #     # d1 = FGSM_attack(model, dataloader)
        #     # response_dict = {'dataset': dataset}
        #     # response_json = pickle.dumps(response_dict)
                
        #     # else:
        #     #     self.send_error(400, "Invalid input. Please send a JSON with an integer 'number'.")
        # except json.JSONDecodeError:
        #     self.send_error(400, "Invalid JSON format. Please send a valid JSON.")

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting http server on {addr}:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()