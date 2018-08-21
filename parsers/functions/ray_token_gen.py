import hashlib


def ray_token_gen(secret, salt, phone_number, session_id, otp_code):
    return str(hashlib.sha512(
        str(secret + salt + phone_number + session_id + otp_code).encode('utf-8')
    ).hexdigest()).upper()


ray_token_gen.__js_name__ = 'rayTokenGenerator'
