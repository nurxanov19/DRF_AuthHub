from django.shortcuts import render
from rest_framework.views import APIView

from methodism import METHODISM
from api_auth import methods


class Main(METHODISM):
    file = methods
    token_key = 'Token'
    not_auth_methods = ['auth_one', 'auth_two', 'register', 'login']
