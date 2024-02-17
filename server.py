from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import torch
import FGSM as attacks
import pickle

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

	def do_POST(self):
		content_length = int(self.headers['Content-Length']) # Gets the size of data
		post_data = self.rfile.read(content_length) # Gets the data itself

		data = pickle.loads(post_data.decode('utf-8'))
		dataloader = data.get('dataloader')
		model = data.get('model')
		options = data.get('options')
		imagenet = options["imagenet"]
		response = dict()
		
		
		# Check if 'number' is a valid integer
		if options["FGSM"]:
			d1, prev_labels = attacks.FGSM_attack(model, dataloader, options["FGSM_batches"]) # returns list, list
			response["FGSM data"] = pickle.dumps(d1)
			response["FGSM labels"] = pickle.dumps(prev_labels)
			response["FGSM image"] = 
		if options["PGD"]:
			d2, prev_labels = attacks.PGD_attack(model, dataloader, options["FGSM_batches"], options['PGD_iterations'])
		if options["targeted"]:
			d3, prev_labels = attacks.targeted_adversarial_attack(model, dataloader, options["targeted_batches"], 
				options["targeted_iterations"], options["targeted_label"])

		response_dict = {'dataset': dataset}
		self.send_response(200)
		self.send_header('Content-type', 'application/pickle')
		self.end_headers()
		reponse = pickle.dumps(response_dict)
		self.wfile.write(response.encode('utf-8'))
			

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, addr="localhost", port=8000):
	server_address = (addr, port)
	httpd = server_class(server_address, handler_class)

	print(f"Starting http server on {addr}:{port}")
	httpd.serve_forever()

if __name__ == "__main__":
	run()