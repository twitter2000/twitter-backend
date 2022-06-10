from rest_framework.decorators import api_view
import json
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import *
from .serializers import *
from django.core.mail import send_mail
import random


# User Registration for new account
@api_view(['POST'])
def user_register(request):

    if request.method == 'POST':
        try:
            username = User.objects.filter(Q(username=request.data['username']) | Q(
                email=request.data['email'])).exists()
            if not username:
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({ 'success': False})
            return JsonResponse({'message': 'The account with username or email is already exists..!', 'success': False})
        except:
            return JsonResponse({'message': 'The account with username or email is already exists..!', 'success': False})
    else:
        return JsonResponse({'message': 'Something went wrong!', 'success': False})


@api_view(['POST'])
def verify_email(request):
    try:
        email = request.data['email']
        # print(email)
        otp_number = random.randint(111111, 999999)

        user = User.objects.get(email=email)
        # print(user)
        forgot = ForgotDetails.objects.create(email=email, otp=otp_number)
        forgot.save()
        # print(forgot)

        send_mail(
            'Know username or change of Password...!',
            f'Hello,Use the following One-time password {otp_number} to reset your password or know username\n{otp_number}',
            'cosquntime@gmail.com',
            [email],
            fail_silently=False,
        )
        print('sent')
        return JsonResponse({'message': 'successfully sent please check mail box!', 'success': True})
    except:
        return JsonResponse({'message': 'The email doesn\'t match, you need an account', 'success': False})


# one time authentication and generation of Token
@api_view(['POST'])
def user_authentication(request):
    username = request.data.get('username')
    password = request.data.get('password')
    print(username, password)
    user = authenticate(username=username, password=password)

    if user:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        token = Token(user=user, ip=ip)
        token.save()
        serializer = TokenSerializer(token)
        return JsonResponse({'data': serializer.data, 'success': True})
    else:
        return JsonResponse({'data': 'Check the Username or password not matched', 'success': False})

# The generated token is used for each api authentication


def user_token(decorate):
    def session(*args, **kwargs):
        request = args[0]
        try:
            print(request.META['HTTP_AUTHORIZATION'].split(' ')[1])
            token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]

        except (KeyError, IndexError):
            return JsonResponse('<h1>Unauthorized(401)</h1>', safe=False)

        try:
            tokenobj = Token.objects.get(session_token=token)
        except Token.DoesNotExist:
            return JsonResponse('<h1>Unauthorized(401)</h1>')

        if tokenobj.session_token == token:
            return decorate(*args, **kwargs)
        else:
            return JsonResponse('<h1>Token Expired(401)</h1>')

    return session


@api_view(['POST'])
def forgot_details(request):
    try:
        type_res = request.data['type']
        if type_res == 'password':
            username = User.objects.filter(username=request.data['username']).update(
                password=request.data['password'])
            return JsonResponse({'password': 'Successfully updated the password', 'success': True})
        elif type_res == 'username':
            email = ForgotDetails.objects.get(otp=request.data['otp']).email
            username = User.objects.get(email=email).username
            ForgotDetails.objects.filter(otp=request.data['otp']).delete()
            print(username)
            return JsonResponse({'username': username, 'success': True})
    except:
        return JsonResponse({'message': 'please check, you have entered a wrong OTP..', 'success': False})
