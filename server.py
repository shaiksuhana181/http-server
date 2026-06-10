import http.server
import socketserver
import urllib.parse
import json

# HTML content for the form page
HTML_CONTENT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Form</title>
</head>
<body>
    <h1>Simple Contact Form</h1>
    <form action="/submit" method="post">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required><br><br>
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required><br><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

# Custom handler to serve the HTML page and process form submissions
class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve the HTML form
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode())
        else:
            # Handle 404 for unknown paths
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Page not found!")

    def do_POST(self):
        if self.path == '/submit':
            # Get the length of the data and read it
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            # Parse the form data
            form_data = urllib.parse.parse_qs(post_data.decode())
            
            # Extract name and email from form data
            name = form_data.get("name", [""])[0]
            email = form_data.get("email", [""])[0]
            
            # Log the form data to a file (append mode)
            with open("submissions.txt", "a") as file:
                file.write(f"Name: {name}, Email: {email}\n")
            
            # Send a success response to the client
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = json.dumps({"status": "success", "message": "Form submitted successfully!"})
            self.wfile.write(response.encode())
        else:
            # Handle 404 for unknown POST paths
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Page not found!")

# Function to start the server
def start_server():
    PORT = 8080
    with socketserver.TCPServer(("localhost", PORT), SimpleHTTPRequestHandler) as httpd:
        print(f"Serving on http://localhost:{PORT}")
        httpd.serve_forever()

# Run the server
if __name__ == "__main__":
    start_server()
