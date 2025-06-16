import random
import re
from django.utils.translation import gettext_lazy as _
from rest_framework.permissions import BasePermission
from django.conf import settings

from exceptions.exception import CustomApiException
from exceptions.error_messages import ErrorCodes



def otp_generate(user):
    from .models import Otp

    otp = Otp.objects.filter(user=user).first()
    if otp:
        response = {
            'otp_code': otp.otp_code,
            'new': False
        }
        return response
    else:
        otp_code = str(random.randint(100000, 999999))
        otp = Otp.objects.create(user=user, otp_code=otp_code)
        otp.save()
        response = {
            'otp_code': otp.otp_code,
            'new': True
        }
        return response


def validate_phone_number(value):
    """
    Validates international phone numbers in E.164 format.
    Example: +998991234567, +12025550123, etc.
    """
    pattern = r'^\+[1-9]\d{3,14}$'
    if not re.fullmatch(pattern, value):
        raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED,
                                 message=_('Invalid phone number. Example: +998991234567, +12025550123, etc.'))


class IsMyBot(BasePermission):
    def has_permission(self, request, view):
        auth_header = request.headers.get("X-Bot-Secret", "")
        expected_token = f"{settings.BOT_SECRET_KEY}"
        return expected_token == auth_header
