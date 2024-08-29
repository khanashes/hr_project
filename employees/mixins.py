from django.core.cache import cache
from rest_framework.exceptions import Throttled

class RateLimitMixin:
    def check_rate_limit(self, request):
        ip = request.META.get('REMOTE_ADDR')
        key = f'rate-limit-{ip}'
        count = cache.get(key, 0)
        if count >= 100:  # Limit to 100 requests per hour
            raise Throttled(detail='Rate limit exceeded.')
        cache.set(key, count + 1, timeout=3600)