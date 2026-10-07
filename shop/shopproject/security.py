from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect


class CsrfProtectedMixin:
    """
    Enforces CSRF checks on a DRF view.

    DRF exempts every view from Django's CSRF middleware and only checks the
    token again for session-authenticated requests. Views that change state
    for anonymous visitors (login, registration, the session cart) would be
    left unprotected, so this mixin puts the check back. Clients must send the
    `csrftoken` cookie value in the `X-CSRFToken` header.
    """

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def csrf_failure(request, reason=""):
    """Reports CSRF failures as JSON, which the React frontend can display."""
    return JsonResponse(
        {"detail": "اعتبار درخواست منقضی شده است. صفحه را دوباره بارگذاری کنید."},
        status=403,
    )
