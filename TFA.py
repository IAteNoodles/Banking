from onetimepass import valid_totp
from secrets import choice


def generate_secret():  # Function to return a random string with length 16.
    secret = ''
    while len(secret) < 16:
        secret += choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ01234567')
    return secret

"""print('Enter the following secret in your authenticator app: ', secret)
Instructions for saving this secret it Google Authenticator:
1. Open Google Authenticator.
2. Click plus icon at the right bottom.
3. Click Enter a setup key.
4. Enter an Account name of your choice and enter the secret provided above.
5. Click Add.
"""
def check_2fa(secret: str, otp: int) -> bool:
    authenticated = valid_totp(otp, secret.encode('utf-8'))
    return authenticated
