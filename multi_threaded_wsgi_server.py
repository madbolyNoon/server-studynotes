import asyncio

# Define an ASGI application
async def asgi_app(scope, receive, send):
    assert scope['type'] == 'http'  # Only handle HTTP connections

    method = scope['method']
    path = scope['path']
    print("ASGI Application: Received scope:", scope) 

    # Respond to GET requests only
    if method == 'GET':
        print(f"Handling GET request at path: {path}")

        if path == '/':
            response_body = b"Hello, World!"
        else:
            response_body = b"Implement it yourself"

        # Send the 200 OK status and headers
        status = '200 OK'
        headers = [(b'content-type', b'text/plain; charset=utf-8')]
        print(f"Sending response with status: {status}")

        # Send the HTTP response start event
        await send({
            'type': 'http.response.start',
            'status': 200,
            'headers': headers,
        })

        # Send the HTTP response body event
        await send({
            'type': 'http.response.body',
            'body': response_body,
        })

    else:
        # If not GET, return 405 Method Not Allowed
        print(f"Method {method} not allowed")
        status = '405 Method Not Allowed'
        headers = [(b'content-type', b'text/plain; charset=utf-8')]

        # Send the HTTP response start event
        await send({
            'type': 'http.response.start',
            'status': 405,
            'headers': headers,
        })

        # Send the HTTP response body event
        await send({
            'type': 'http.response.body',
            'body': b'Method not allowed',
        })

# Function to run the ASGI server
async def run_asgi_server(app):
    server = await asyncio.start_server(
        lambda reader, writer: handle_asgi_connection(app, reader, writer),
        '127.0.0.1', 8000
    )
    print("Serving on port 8000...")

    async with server:
        await server.serve_forever()

# Handle the ASGI connection and process HTTP events
async def handle_asgi_connection(app, reader, writer):
    try:
        # Receive request data from the client
        print("Waiting to receive request data from the client...")
        request_data = await reader.read(1024)

        # Decode and parse the request
        request_text = request_data.decode('utf-8')
        print("Decoded request data:", request_text)
        headers = request_text.splitlines()
        request_line = headers[0]
        method, path, _ = request_line.split()

        # Define ASGI scope
        scope = {
            'type': 'http',
            'method': method,
            'path': path,
            'headers': [],
        }

        # Define async receive and send functions for ASGI
        async def receive():
            # ASGI receive is only needed for request bodies (optional in this case)
            return {'type': 'http.request'}

        async def send(message):
            # ASGI send function to handle different message types
            if message['type'] == 'http.response.start':
                status = message['status']
                headers = message['headers']
                writer.write(f"HTTP/1.1 {status} OK\r\n".encode('utf-8'))
                for header in headers:
                    writer.write(f"{header[0].decode()}: {header[1].decode()}\r\n".encode('utf-8'))
                writer.write(b"\r\n")  # End of headers

            elif message['type'] == 'http.response.body':
                body = message.get('body', b'')
                writer.write(body)
                await writer.drain()

        # Call the ASGI app
        await app(scope, receive, send)

    except Exception as e:
        print(f"Error handling request: {e}")

    finally:
        # Close the client connection
        print("Closing the client connection.")
        writer.close()
        await writer.wait_closed()

# Run the server
if __name__ == '__main__':
    asyncio.run(run_asgi_server(asgi_app))