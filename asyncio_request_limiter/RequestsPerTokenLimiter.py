import asyncio
from collections import defaultdict


class RequestsPerTokenLimiter:
    _token = None
    _limits = None
    _locks = defaultdict(lambda: asyncio.Lock())
    _times = defaultdict(lambda: 0)
    _debug = False

    @property
    def _lock(self):
        """Lock to prevent multiple requests through a single token."""
        return self._locks[self._token]

    def __init__(self, limits, token=None, debug=False):
        self._limits = limits
        self._token = token
        self._debug = debug

    async def __aenter__(self):
        if not self._token:
            raise Exception("Token missed. Use: `with RequestsPerTokenLimiter(LIMITS, token='your token'):`.")

        await self._lock

        to_wait = self._to_wait_before_request()

        if self._debug:
            print(f'[{self._token}]: wait {to_wait} sec before next request.')

        await asyncio.sleep(to_wait)

    async def __aexit__(self, *args):
        if self._debug:
            print(f'[{self._token}]: request just finished.')

        self._update_request_time()
        self._lock.release()

    def _to_wait_before_request(self):
        """Calculate time to sleep before next requests."""
        request_time = self._times[self._token]
        request_delay = 1 / self._limits[self._token]
        now = asyncio.get_event_loop().time()
        to_wait = request_time + request_delay - now
        to_wait = max(0, to_wait)
        return to_wait

    def _update_request_time(self):
        now = asyncio.get_event_loop().time()
        self._times[self._token] = now
