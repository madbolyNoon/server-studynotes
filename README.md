Here’s a complete README draft with additional details to provide more context around asyncio, ASGI vs. WSGI, and components of asyncio.

Madboly’s Study Notes

This repository is a personal exploration of asynchronous and synchronous programming paradigms in Python, focusing on the foundational concepts that lead up to understanding Uvicorn, an ASGI server, and Starlette, an ASGI framework.

Since synchronous programming came before Asynchronous programming, we’ll start with synchronous concepts.

	The target is to understand Uvicorn, which is built on Starlette.

Starlette: Starlette is an ASGI web framework designed for building fast, lightweight, asynchronous applications in Python. ASGI stands for Asynchronous Server Gateway Interface and is a standard that enables asynchronous Python web frameworks and applications to communicate with servers in a non-blocking way.

	In the current line of thought, ASGI seems like WSGI with added asyncio capabilities. We’ll explore below to see how accurate that is.

Key Differences Between ASGI and WSGI

	•	WSGI (Web Server Gateway Interface):
	•	WSGI is a specification for synchronous web applications in Python. It supports one request at a time per thread, making it suitable for traditional synchronous frameworks like Flask and Django (pre-async updates).
	•	WSGI servers (such as Gunicorn and uWSGI) are limited by this synchronous nature, which restricts their use for handling tasks requiring long-lived connections, like WebSockets.
	•	ASGI (Asynchronous Server Gateway Interface):
	•	ASGI is an evolution of WSGI, created to support asynchronous frameworks and long-lived connection types, like WebSockets and HTTP/2.
	•	ASGI applications can run both synchronous and asynchronous code, allowing frameworks like Starlette and FastAPI to manage concurrent requests efficiently, thanks to the event-driven nature of asynchronous programming with asyncio.

Asyncio and Asynchronous Programming

Why Use Asyncio?

asyncio is a foundational library in Python that enables asynchronous programming through the async/await syntax. This approach is particularly useful for applications with significant I/O operations—such as making network requests, reading files, or handling user input—because it allows the program to perform other tasks while waiting for I/O to complete.

What’s the Difference Between Multithreading and Asyncio?

	•	Multithreading:
	•	In Python, multithreading allows multiple threads to execute tasks concurrently.
	•	However, due to Python’s Global Interpreter Lock (GIL) in CPython, only one thread can execute Python bytecode at a time, which often limits the effectiveness of multithreading for CPU-bound tasks.
	•	While multithreading can work well for I/O-bound tasks, it also comes with the overhead of managing multiple threads and dealing with potential concurrency issues (e.g., race conditions).
	•	Asyncio:
	•	asyncio operates on a single thread but achieves concurrency through coroutines. When a coroutine hits an await statement, it pauses, allowing the event loop to continue executing other coroutines that are ready.
	•	This event-driven approach is more efficient for I/O-bound tasks as it avoids the need for multiple threads, reducing memory usage and the risk of concurrency issues.
	•	Ideal for handling numerous concurrent tasks, asyncio enables smooth handling of requests, especially for web applications with high I/O demands.

Components of Asyncio

Understanding some core components of asyncio can help in writing efficient asynchronous applications:

	•	Event Loop:
	•	The asyncio event loop orchestrates the execution of asynchronous tasks. It cycles through tasks, checking if they are ready to run or waiting on I/O operations. When a coroutine awaits an operation, the loop temporarily pauses it and continues to other tasks.
	•	Coroutines:
	•	Coroutines, defined using async def, are functions that can be paused and resumed. By yielding control with await, they enable concurrent execution within a single thread.
	•	Tasks:
	•	asyncio tasks allow coroutines to run concurrently. By using asyncio.create_task(coroutine), a coroutine is scheduled to run in the background, letting the event loop manage it while other tasks continue.
	•	Futures and Promises:
	•	In asyncio, a Future is an object that represents a value that isn’t available yet but will be in the future. When a coroutine awaits a Future, it pauses until the Future is resolved (e.g., when an I/O operation completes). This is fundamental for handling asynchronous responses.
	•	Await:
	•	The await keyword pauses a coroutine until the awaited task completes. This keyword is the primary tool for achieving non-blocking behavior, letting the event loop handle other tasks while waiting.

Moving Towards ASGI and Uvicorn

ASGI-based servers like Uvicorn extend these concepts to web applications, where multiple connections, requests, and responses can be managed concurrently in a non-blocking manner. Uvicorn uses the power of asyncio to handle a large number of simultaneous connections efficiently, making it a go-to choice for ASGI frameworks like Starlette and FastAPI.

By understanding the principles of asyncio and asynchronous programming, we build a foundation for more advanced, high-performance applications with ASGI-compatible servers and frameworks.