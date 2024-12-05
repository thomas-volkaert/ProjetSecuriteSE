from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Check if content type is multipart/form-data
        content_type = self.headers.get('Content-Type')
        if not content_type or "multipart/form-data" not in content_type:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Unsupported Content-Type")
            return

        # Parse boundary from content type
        boundary = content_type.split("boundary=")[-1].encode()
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        # Split body by boundary to separate parts
        parts = body.split(b'--' + boundary)
        
        for part in parts:
            # Ignore empty parts and the last boundary marker
            if not part or part == b'--\r\n':
                continue

            # Extract headers and file content
            headers, file_data = part.split(b'\r\n\r\n', 1)
            headers = headers.decode().split('\r\n')
            
            # Find filename in Content-Disposition header
            for header in headers:
                if header.startswith("Content-Disposition"):
                    if 'filename="' in header:
                        filename = header.split('filename="')[-1].split('"')[0]
                        filename = os.path.basename(filename)  # sanitize the filename
                        break
            else:
                # No filename found in part
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"No file found in the request.")
                return

            # Save the file data, excluding the final CRLF
            with open(filename, "wb") as f:
                f.write(file_data.rstrip(b'\r\n'))

        # Send success response
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"File received and saved.")

# Configure the server to listen on localhost:8000
def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print("Starting server on port 8000...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
