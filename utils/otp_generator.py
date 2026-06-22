import time
import pyotp
from config.settings import MFA_SECRET


def get_fresh_otp():
    secret = MFA_SECRET.replace(" ", "").strip()

    totp = pyotp.TOTP(
        secret,
        digits=6,
        interval=30,
        digest="sha1"
    )

    remaining = 30 - (int(time.time()) % 30)

    # Wait for next fresh OTP if current one is close to expiry
    if remaining <= 15:
        time.sleep(remaining + 1)

    otp = totp.now()
    print("Remaining seconds:", 30 - (int(time.time()) % 30))
    print("Generated OTP:", otp)

    return otp