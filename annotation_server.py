#!/usr/bin/env python3
"""
Simple HTTP server for handling annotation file saves
"""
import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import datetime

class AnnotationHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/save_annotations':
            self.handle_save_annotations()
        else:
            self.send_error(404, "Not found")
    
    def handle_save_annotations(self):
        try:
            # Read the request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            # Create annotations directory if it doesn't exist
            annotations_dir = 'annotations'
            if not os.path.exists(annotations_dir):
                os.makedirs(annotations_dir)
            
            # Save the file
            filename = data.get('filename', f'annotations_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
            filepath = os.path.join(annotations_dir, filename)
            
            with open(filepath, 'w') as f:
                json.dump(data['data'], f, indent=2)
            
            # Send success response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'success': True,
                'filepath': filepath,
                'message': f'Annotations saved to {filepath}'
            }
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            # Send error response
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'success': False,
                'error': str(e)
            }
            self.wfile.write(json.dumps(response).encode())
    
    def end_headers(self):
        # Add CORS headers to allow cross-origin requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.end_headers()

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, AnnotationHandler)
    print(f"Starting annotation server on port {port}")
    print(f"Annotation files will be saved to: {os.path.abspath('annotations')}")
    print(f"Open http://localhost:{port}/viewer.html in your browser")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()

if __name__ == '__main__':
    port = 8000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    run_server(port) 