# Madboly’s Study Notes

This repository is a personal exploration of **asynchronous** and **synchronous programming paradigms** in Python. It primarily focuses on foundational concepts leading to an understanding of **Uvicorn**, an ASGI server, and **Starlette**, an ASGI framework.

## Overview

Since synchronous programming predates asynchronous programming, this study begins with synchronous concepts to build a strong foundation.

> The target is to understand **Uvicorn**, which is built on **Starlette**.

### What is Starlette?
**Starlette** is an ASGI web framework designed for building fast, lightweight, asynchronous applications in Python. ASGI, or **Asynchronous Server Gateway Interface**, is a standard enabling asynchronous Python web frameworks and applications to communicate with servers in a non-blocking way.

In simpler terms, ASGI is comparable to **WSGI** but with added **asyncio capabilities**. This study will explore how true that comparison is.

## Key Differences Between ASGI and WSGI

| WSGI (Web Server Gateway Interface)                                                                                         | ASGI (Asynchronous Server Gateway Interface)                                                                                           |
|-----------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| **Synchronous** specification for web applications in Python.                                                               | **Evolution** of WSGI, supporting asynchronous frameworks and long-lived connection types (e.g., WebSockets, HTTP/2).                  |
| Supports one request per thread, ideal for traditional synchronous frameworks (Flask, Django pre-async updates).            | Allows both **synchronous** and **asynchronous** code execution, enabling frameworks like **Starlette** and **FastAPI**.               |
| Limited for long-lived connections due to its synchronous nature. Examples: **Gunicorn** and **uWSGI**.                    | More **efficient** for concurrent requests thanks to its event-driven nature. Optimized for high **I/O demands** using **asyncio**.   |

---

## Asyncio and Asynchronous Programming

### Why Use Asyncio?
`asyncio` is a foundational library in Python that enables asynchronous programming through `async/await` syntax. It is particularly effective for **I/O-bound** applications, such as:

- **Network requests**
- **File operations**
- **Handling user input**

Using asyncio allows the program to **perform other tasks while waiting for I/O** to complete.

### What’s the Difference Between Multithreading and Asyncio?

| **Multithreading**                                                                                                 | **Asyncio**                                                                                                                      |
|---------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| Allows multiple threads to run concurrently but is limited by Python’s **Global Interpreter Lock (GIL)** in CPython. | Runs on a **single thread** using coroutines, pausing at `await` statements to handle other tasks within a single event loop.     |
| Works well for I/O-bound tasks but introduces complexity with **race conditions** and **thread management**.        | More efficient for I/O-bound tasks as it avoids the need for multiple threads, reducing memory usage and concurrency issues.      |
| Less effective for **CPU-bound tasks** due to GIL limitations.                                                      | Ideal for managing **numerous concurrent I/O tasks** in web applications.                                                         |

---

## Components of Asyncio

Async componenents:
> everything is coroutines and boiles down to job scheduling between cpu and *coroutines*
- **Event Loop**: Orchestrates the execution of asynchronous tasks. It cycles through tasks, running those ready or awaiting I/O operations.
- **Coroutines**: Defined using `async def`, they can be paused and resumed, allowing concurrent execution within a single thread.
- **Tasks**: Enable concurrent execution of coroutines. Created using `asyncio.create_task(coroutine)`, allowing coroutines to run in the background.
- **Futures and Promises**: Represent values not yet available (e.g., awaiting I/O operations). When a coroutine awaits a Future, it pauses until the operation completes.
- **Await**: The `await` keyword pauses a coroutine until the awaited task completes, allowing non-blocking behavior.

---

## Moving Towards ASGI and Uvicorn

ASGI-based servers like **Uvicorn** leverage these asyncio concepts to support web applications handling numerous connections in a non-blocking way. Uvicorn’s efficient handling of connections makes it ideal for ASGI frameworks such as **Starlette** and **FastAPI**.

---

> **Note:** This document is a work in progress and will be expanded with further insights.

