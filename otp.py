import os
import secrets
import string
import time
from flask import Flask, session
import requests


def generate_otp(length=6):
    digits = string.digits
    return ''.join(secrets.choice(digits) for _ in range(length))


def send_otp_sms(phone_number):
    if not phone_number:
        return {
            "success": False,
            "error": "Phone number is required for OTP verification."
        }

    otp_code = generate_otp()

    session['otp'] = otp_code
    session['otp_expires_at'] = time.time() + (10 * 60)
    session['otp_verified'] = False

    message_text = (
        f"Your registering to ActBayan!, Your verification code is: {otp_code}. "
        f"It will expire in 10 minutes. Do not share this code."
    )

    api_key = os.environ.get('TEXTBEE_API_KEY', 'txb_1PEJCKYRqeIGtyVTCFS0mNxvei5Y8OX7')

    if not api_key:
        return {
            "success": False,
            "error": "TEXTBEE_API_KEY is missing."
        }

    try:
        res = requests.post(
            'https://api.textbee.dev/api/v1/gateway/send-sms',
            headers={
                'x-api-key': api_key
            },
            json={
                'deviceId': '6ac7151c2597187c9c33ca6e',
                'recipients': [phone_number],
                'message': message_text
            },
            timeout=15
        )

        res.raise_for_status()

        return {
            "success": True,
            "api_response": res.json()
        }

    except requests.exceptions.RequestException as e:
        session.pop('otp', None)
        session.pop('otp_expires_at', None)

        return {
            "success": False,
            "error": str(e)
        }