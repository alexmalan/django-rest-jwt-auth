"""
User services.
"""
from rest_framework.exceptions import ValidationError

from .models import User


def deposit_amount(user=None, amount=None):
    """
    Deposit amount to user's deposit

    :param User user: User instance
    :param int amount: Amount to deposit
    """
    if (
        amount is None
        or not isinstance(amount, int)
        or amount not in [100, 50, 20, 10, 5]
    ):
        raise ValidationError("Invalid input")

    user.deposit += amount
    try:
        user.save()
    except Exception:
        raise ValidationError("Error while saving the user")

    return True


def reset_amount(user=None):
    """
    Reset user's deposit

    :param User user: User instance
    """
    if user is None or not isinstance(user, User):
        raise ValidationError("Invalid input")

    user.deposit = 0
    try:
        user.save()
    except Exception:
        raise ValidationError("Error while saving the user")

    return True
