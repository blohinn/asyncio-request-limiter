from setuptools import setup, find_packages

setup(
    name='asyncio-request-limiter',
    description='The main purpose of this lib to help you avoid errors like "to many requests per second" on many amount of async requests. Check GitHub repo for documentation.',
    version='1.0.1',
    packages=find_packages(),
    author='Ivan Blohin',
    author_email='ivan.blohinn@yandex.ru',
    url='https://github.com/blohinn/asyncio-request-limiter',
)
