import random
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from .models import User, Otp


def otp_generate(user):
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

def decode_token(token):
    try:
        payload = UntypedToken(token)
        return payload
    except TokenError:
        return

def validate_token(token):
    if not token:
        return
    if len(token.split()) < 2 or token.split()[0] != 'Bearer':
        return
    if decode_token(token.split()[1]) is None:
        return
    user_id = decode_token(token.split()[1]).get('user_id', None)
    login_time = decode_token(token.split()[1]).get('login_time', None)
    if user_id is None or login_time is None:
        return
    if User.objects.filter(id=user_id, login_time=login_time).exists():
        return decode_token(token.split()[1])
