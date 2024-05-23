from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from html import escape
import json
import threading

class MessageHandler(BaseHTTPRequestHandler):
    messages = []

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'''
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Simple Messaging Service</title>
                    <script>
                        function refreshMessages() {
                            var xhr = new XMLHttpRequest();
                            xhr.open('GET', '/messages', true);
                            xhr.onreadystatechange = function() {
                                if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                                    var messages = JSON.parse(xhr.responseText);
                                    var messageList = document.getElementById('messages');
                                    messageList.innerHTML = '';
                                    messages.forEach(function(msg) {
                                        var li = document.createElement('li');
                                        li.textContent = msg;
                                        messageList.appendChild(li);
                                    });
                                }
                            };
                            xhr.send();
                        }
                        setInterval(refreshMessages, 3000); // Refresh every 3 seconds
                    </script>
                </head>
                <body>
                    <h1>Simple Messaging Service</h1>
                    
                    <h2>Send a Message</h2>
                    <form action="/send_message" method="post">
                        <input type="text" name="message" placeholder="Enter your message" required>
                        <button type="submit">Send</button>
                    </form>

                    <h2>Messages</h2>
                    <ul id="messages">
                        <!-- Messages will be displayed here -->
                    </ul>
                </body>
                </html>
            ''')

        elif self.path == '/messages':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(self.messages).encode('utf-8'))

    def do_POST(self):
        if self.path == '/send_message':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            post_params = parse_qs(post_data.decode('utf-8'))
            message = post_params['message'][0]
            self.messages.append(message)
            self.send_response(303)  # Redirect after POST
            self.send_header('Location', '/')
            self.end_headers()

def run(server_class=HTTPServer, handler_class=MessageHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    threading.Thread(target=httpd.serve_forever).start()

if __name__ == '__main__':
    run()
