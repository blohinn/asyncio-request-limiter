from urllib.parse import urlparse

from .RequestsPerTokenLimiter import RequestsPerTokenLimiter


class RequestsPerHostLimiter(RequestsPerTokenLimiter):

    def __init__(self, limits, url, debug=False):
        super(RequestsPerHostLimiter, self).__init__(
            limits=limits,
            token=urlparse(url).hostname,
            debug=debug
        )
