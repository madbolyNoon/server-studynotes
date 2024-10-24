import socket

# Define a simple WSGI application
def simple_app(environ, start_response):
    print("WSGI Application: Received environ:", environ) 
    
    method = environ['REQUEST_METHOD']
    path = environ['PATH_INFO']

    # Respond to GET requests only
    if method == 'GET':
        print(f"Handling GET request at path: {path}")
        
        if path == '/':
            response_body = b"Hello, World!"
        else:
            response_body = b"Implement it yourself"
        
        # Send the 200 OK status and headers
        status = '200 OK'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        print(f"Sending response with status: {status}")
        start_response(status, headers)
        return [response_body]

    else:
        # If not GET, return 405 Method Not Allowed
        print(f"Method {method} not allowed")
        status = '405 Method Not Allowed'
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return [b'Method not allowed']

# Function to handle HTTP requests and serve WSGI responses
def handle_request(client_socket):
    try:
        # Receive request data from the client
        print("Waiting to receive request data from the client...")
        request_data = client_socket.recv(1024)

        # Decode the received bytes to a string
        request_data = request_data.decode('utf-8')
        print("Decoded request data:", request_data)

        # Check if the request data is empty
        if not request_data:
            print("No data received, returning.")
            return
        
        # Split request data into lines (headers and request line)
        headers = request_data.splitlines()
        print("Request headers:", headers)

        # Parse the first line of the request (e.g., "GET / HTTP/1.1")
        request_line = headers[0]
        print("Request line:", request_line)
        
        method, path, _ = request_line.split()

        # Create a WSGI environment dictionary
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': path
        }

        print("Created WSGI environ:", environ)

        # Define a start_response function
        def start_response(status, response_headers):
            print(f"start_response called with status: {status}")
            print("Response headers:", response_headers)
            
            # Send the status line and headers
            client_socket.send(f"HTTP/1.1 {status}\r\n".encode('utf-8'))
            for header in response_headers:
                client_socket.send(f"{header[0]}: {header[1]}\r\n".encode('utf-8'))
            client_socket.send(b"\r\n")  # End of headers

        # Call the WSGI application and send the response body
        response_body = simple_app(environ, start_response)
        
        # Send the response body to the client
        print("Sending response body to the client...")
        for body in response_body:
            client_socket.send(body)

        print("Response sent successfully.")

    except Exception as e:
        print(f"Error handling request: {e}")

    finally:
        # Close the client connection
        print("Closing the client connection.")
        client_socket.close()

# Function to start the WSGI server using raw sockets
def run_server():
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to localhost:8000
    server_socket.bind(('127.0.0.1', 8000))
    server_socket.listen(5)
    print("Serving on port 8000...")

    # Server loop to handle incoming connections
    while True:
        try:
            # Accept client connections
            print("\nWaiting for a new client connection...")
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")

            # Handle the incoming request
            handle_request(client_socket)

        except KeyboardInterrupt:
            print("\nShutting down the server.")
            break

    # Close the server socket
    server_socket.close()

# Run the server
if __name__ == '__main__':
    run_server()