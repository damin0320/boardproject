import json
import bcrypt
import jwt
import re
from json import JSONDecodeError

from django.views import View
from django.http import JsonResponse

from .models import Member
from my_settings import SECRET_KEY, HASHING_ALGORITHM


class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            member = Member.objects.get(name=data['name'])
            password = data['password']

            if bcrypt.checkpw(password.encode('utf-8'), member.password.encode('utf-8')):
                token = jwt.encode({'member_id': member.id}, SECRET_KEY, algorithm=HASHING_ALGORITHM)
                return JsonResponse({'token': token, 'message': 'SUCCESS'}, status=200)
            return JsonResponse({'message': 'INVALID_USER'}, status=401)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except Member.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXIST'}, status=401)


class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            name = data['name']
            email = data['email']
            password = data['password']

            if not name or not email or not password:
                return JsonResponse({'message': 'EMPTY_VALUE'}, status=400)

            p_name = re.compile(r'^[a-zA-Z0-9_-]{2,20}$')
            p_email = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z-.]+$')
            p_password = re.compile(r'^(?=.*[!-/:-@])(?!.*[ㄱ-ㅣ가-힣]).{8,20}$')

            if not p_name.match(name):
                return JsonResponse({'message': 'INVALID_NAME_FORMAT'}, status=400)
            if not p_email.match(email):
                return JsonResponse({'message': 'INVALID_EMAIL_FORMAT'}, status=400)
            if not p_password.match(password):
                return JsonResponse({'message': 'INVALID_PASSWORD_FORMAT'}, status=400)
            if Member.objects.filter(email=email).exists():
                return JsonResponse({'message': 'EXISTING_EMAIL'}, status=400)
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            decoded_hashed_pw = hashed_pw.decode('utf-8')

            Member.objects.create(
                name=name,
                password=decoded_hashed_pw,
                email=email
            )
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSON_DECODE_ERROR'}, status=400)