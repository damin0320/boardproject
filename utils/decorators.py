import json
import jwt
from jwt.exceptions import InvalidSignatureError, DecodeError

from django.http import JsonResponse

from member.models import Member
from boardproject.settings import SECRET_KEY, HASHING_ALGORITHM


# auth check with blocking
def auth_check(func):
    def wrapper(self, request):
        try:
            token = request.headers.get('Authorization')
            if not token:
                return JsonResponse({'message': 'TOKEN_DOES_NOT_EXIST'}, status=400)

            decoded_auth_token = jwt.decode(token, SECRET_KEY, algorithms=HASHING_ALGORITHM)
            member_id = decoded_auth_token['member_id']
            member = Member.objects.get(id=member_id)

            request.member = member
            return func(self, request)

        except InvalidSignatureError:
            return JsonResponse({'message': 'SIGNATURE_VERIFICATION_FAILED'}, status=400)
        except DecodeError:
            return JsonResponse({'message': 'DECODE_ERROR'}, status=400)
        except Member.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXIST'}, status=404)

    return wrapper


# user check without blocking
def user_check(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            if not token:
                request.user = None
                return func(self, request, *args, **kwargs)
            decoded_auth_token = jwt.decode(token, SECRET_KEY, algorithms=HASHING_ALGORITHM)

            member_id = decoded_auth_token['member_id']
            member = Member.objects.get(id=member_id)

            request.member = member
            return func(self, request, *args, **kwargs)

        except InvalidSignatureError:
            return JsonResponse({'message': 'SIGNATURE_VERIFICATION_FAILED'}, status=400)
        except DecodeError:
            return JsonResponse({'message': 'DECODE_ERROR'}, status=400)
        except Member.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXIST'}, stauts=404)

    return wrapper