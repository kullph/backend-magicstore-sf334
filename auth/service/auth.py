from fastapi import HTTPException
import hashlib
import os
from jose import jwt
from datetime import datetime, timedelta, timezone
import requests
import math

class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        sha256 = hashlib.sha256()
        sha256.update(password.encode('utf-8'))
        return sha256.hexdigest()

    @staticmethod
    def create_token(email: str, exp_duration: timedelta) -> str:
        payload = {
            "sub": email,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + exp_duration 
        }
        return AuthService.encode_jwt(payload)

    @staticmethod
    def encode_jwt(payload: dict) -> str:
        secret = os.getenv("JWT_SECRET", "your_default_secret")
        algorithm = "HS256"
        return jwt.encode(payload, secret, algorithm=algorithm)

    @staticmethod
    def decode_jwt(token: str) -> str:
        secret = os.getenv("JWT_SECRET", "your_default_secret")
        algorithm = "HS256"
        try:
            decoded = jwt.decode(token, secret, algorithms=[algorithm])
            return decoded
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Could not validate token")
        
    @staticmethod
    def sentimental(text: str) -> int:
        url = "https://api.aiforthai.in.th/ssense"
        data = {'text':text}
        headers = {
        'Apikey': "AYisycokK7O5mby9enmQ37NxQaLSGd64"
        }
        response = requests.post(url, data=data, headers=headers)
        x = response.json()
        if x['sentiment']['polarity'] == 'positive':
            result = x['sentiment']['score']
            return int(math.floor(float(result)))
        elif x['sentiment']['polarity'] == 'negative':
            result = x['sentiment']['score']
            return -int(math.floor(float(result)))
        else:
            result = x['sentiment']['score']
            return int(math.floor(float(result)))