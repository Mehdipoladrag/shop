from decimal import Decimal

HUNDRED = Decimal(100)
MAX_OFFER_PERCENT = 100


def clamp_offer(offer):
    """A discount is a percentage between 0 and 100, whatever the admin typed."""
    return min(max(int(offer or 0), 0), MAX_OFFER_PERCENT)


def discounted_price(price, offer):
    """Price after the percentage discount."""
    return price - price * Decimal(clamp_offer(offer)) / HUNDRED
