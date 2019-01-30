# AsyncIO Request Limiter
The main purpose of this lib to help you avoid errors like "to many requests per second" on many amount of async requests.

## Features
- Limit requests per second for token (if you make api requests);
- Limit requests per second to host (if you make requests to web site (scraping, for example));

## Installation
```pip install asyncio-request-limiter```

## Usage
##### For token:
```python
import asyncio
from asyncio_request_limiter import RequestsPerTokenLimiter

LIMITS = {
    'token1': 1,  # One request per second with this token
    'token2': 5   # Five requests per second with this token
}


async def get_some_data_from_web(iterr):
    token = 'token1' if iterr % 2 == 0 else 'token2'
    async with RequestsPerTokenLimiter(LIMITS, token=token, debug=True):
        print('Get some data from api...')

tasks = []
loop = asyncio.get_event_loop()

for i in range(10):
    task = asyncio.ensure_future(
        get_some_data_from_web(i)
    )
    tasks.append(task)

loop.run_until_complete(asyncio.gather(*tasks))
```
Output:
```text
[token1]: wait 0 sec before next request.
[token2]: wait 0 sec before next request.
Get some data from web...
[token1]: request just finished.
Get some data from web...
[token2]: request just finished.
[token1]: wait 0.9996501129935496 sec before next request.
[token2]: wait 0.19967552000889555 sec before next request.
Get some data from web...
[token2]: request just finished.
[token2]: wait 0.19991010701050982 sec before next request.
Get some data from web...
[token2]: request just finished.
[token2]: wait 0.19991511706029996 sec before next request.
Get some data from web...
[token2]: request just finished.
[token2]: wait 0.19995121599640697 sec before next request.
Get some data from web...
[token2]: request just finished.
Get some data from web...
[token1]: request just finished.
[token1]: wait 0.9999531270004809 sec before next request.
Get some data from web...
[token1]: request just finished.
[token1]: wait 0.9999459949904121 sec before next request.
Get some data from web...
[token1]: request just finished.
[token1]: wait 0.9998961159726605 sec before next request.
Get some data from web...
[token1]: request just finished.
```
##### For host:
```python
import asyncio
from asyncio_request_limiter import RequestsPerHostLimiter

LIMITS = {
    'jsonplaceholder.typicode.com': 1,  # One request per second to this host
    'httpbin.org': 5   # Five requests per second to this host
}


async def get_some_data_from_web(i):
    if i % 2 == 0:
        url = 'https://jsonplaceholder.typicode.com/todos/1'
    else:
        url = 'https://httpbin.org/get'
    async with RequestsPerHostLimiter(LIMITS, url=url, debug=True):
        print('Get some data from web...')


tasks = []
loop = asyncio.get_event_loop()

for i in range(10):
    task = asyncio.ensure_future(
        get_some_data_from_web(i)
    )
    tasks.append(task)

loop.run_until_complete(asyncio.gather(*tasks))
```
Output:
```text
[jsonplaceholder.typicode.com]: wait 0 sec before next request.
[httpbin.org]: wait 0 sec before next request.
Get some data from web...
[jsonplaceholder.typicode.com]: request just finished.
Get some data from web...
[httpbin.org]: request just finished.
[jsonplaceholder.typicode.com]: wait 0.999491096008569 sec before next request.
[httpbin.org]: wait 0.1995754429954104 sec before next request.
Get some data from web...
[httpbin.org]: request just finished.
[httpbin.org]: wait 0.19991840905277058 sec before next request.
Get some data from web...
[httpbin.org]: request just finished.
[httpbin.org]: wait 0.19993908802280203 sec before next request.
Get some data from web...
[httpbin.org]: request just finished.
[httpbin.org]: wait 0.1999552029883489 sec before next request.
Get some data from web...
[httpbin.org]: request just finished.
Get some data from web...
[jsonplaceholder.typicode.com]: request just finished.
[jsonplaceholder.typicode.com]: wait 0.999923570023384 sec before next request.
Get some data from web...
[jsonplaceholder.typicode.com]: request just finished.
[jsonplaceholder.typicode.com]: wait 0.9999282530043274 sec before next request.
Get some data from web...
[jsonplaceholder.typicode.com]: request just finished.
[jsonplaceholder.typicode.com]: wait 0.9999441289692186 sec before next request.
Get some data from web...
[jsonplaceholder.typicode.com]: request just finished.
```