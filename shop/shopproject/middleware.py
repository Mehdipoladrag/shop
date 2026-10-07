from django.utils.cache import add_never_cache_headers

API_PATH_MARKER = "/api/"


class NoCacheApiMiddleware:
    """
    Keeps API responses out of the site-wide cache.

    The cache middleware stores GET responses by URL only, so an admin API
    response cached for one request would be served to anyone requesting the
    same URL, including anonymous users, and lists would stay stale after edits.
    This middleware must be listed right after UpdateCacheMiddleware so that
    it runs before the response is cached.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if API_PATH_MARKER in request.path:
            add_never_cache_headers(response)
        return response
