import datetime

from jose import ExpiredSignatureError, jwt

from app import config

from .models import User

settings = config.get_settings()


def authenticate(email, password):
    """
    Step 1: Verify the user's credentials
    """
    try:
        user_obj = User.objects.get(email=email)
    except Exception as e:
        user_obj = None
    if not user_obj.verify_password(password):
        return None
    return user_obj


def login(user_obj, expires=5):
    """
    Step 2: After the user is authenticated, log the user in
    and get the user's token for the session that they are working on
    """
    raw_data = {
        "user_id": f"{user_obj.user_id}",
        "role": "admin",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=expires),
    }
    token = jwt.encode(raw_data, settings.secret_key, algorithm=settings.jwt_algorithm)
    return token


def verify_user_id(token):
    """
    Step 3: Verifying the user's login session
    """
    data = None
    try:
        data = jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
    except ExpiredSignatureError as e:
        print(e)
    except:
        pass
    if "user_id" not in data:
        return None
    return data
