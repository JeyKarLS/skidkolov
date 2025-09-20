import hmac
import hashlib
from typing import Optional
from fastapi import HTTPException
import os

# Bot token from env
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here")  # Set in env

def verify_telegram_data(init_data: str) -> dict:
    """
    Verify Telegram WebApp initData
    """
    if not init_data:
        raise HTTPException(status_code=400, detail="No init data")

    try:
        # Parse init_data
        data = {}
        for pair in init_data.split('&'):
            key, value = pair.split('=', 1)
            data[key] = value

        hash_value = data.pop('hash', None)
        if not hash_value:
            raise HTTPException(status_code=400, detail="No hash in init data")

        # Sort data
        data_check_string = '\n'.join(f"{k}={v}" for k, v in sorted(data.items()))

        # Calculate hash
        secret_key = hmac.new('WebAppData'.encode(), BOT_TOKEN.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        if calculated_hash != hash_value:
            raise HTTPException(status_code=401, detail="Invalid hash")

        return data

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid init data")

def get_user_from_init_data(init_data: str) -> dict:
    data = verify_telegram_data(init_data)
    user = data.get('user')
    if not user:
        raise HTTPException(status_code=400, detail="No user in init data")
    # Parse user JSON
    import json
    user_data = json.loads(user)
    return user_data