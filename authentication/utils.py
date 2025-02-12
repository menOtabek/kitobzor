import random

def otp_generate(user):
    otp_code = str(random.randint(100000, 999999))
    user.otp_code = otp_code
    user.save()
    return otp_code