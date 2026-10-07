from rest_framework.throttling import AnonRateThrottle


class LoginThrottle(AnonRateThrottle):
    """Slows down password guessing on the login endpoints."""

    scope = "customer_login"
    rate = "10/min"


class RegisterThrottle(AnonRateThrottle):
    scope = "customer_register"
    rate = "10/hour"
