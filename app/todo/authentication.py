import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings


def generateToken(user):
    payload = {
        "username": user["username"],
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5), 
    }

    return jwt.encode(
        payload=payload, key=getattr(settings, "SECRET_KEY"), algorithm="HS256"
    )


def refreshToken(user):
    return generateToken(user)


def verifyToken(token):
    error_code = 0
    payload = None
    try:
        payload = jwt.decode(
            jwt=token, key=getattr(settings, "SECRET_KEY"), algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        error_code = 1
    except jwt.InvalidTokenError:
        error_code = 2

    return [error_code, payload]


def get_remaining_time(token):
    payload = jwt.decode(
        token, key=getattr(settings, "SECRET_KEY"), algorithms=["HS256"]
    )
    exp_timestamp = payload["exp"]
    exp_datetime = timezone.datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
    remaining_time = exp_datetime - timezone.now()
    return remaining_time


def should_refresh_token(token):
    remaining_time = get_remaining_time(token)
    refresh_threshold = timedelta(
        minutes=5
    )  # Defina um limite de tempo para atualização do token
    return remaining_time < refresh_threshold
