from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.sites.shortcuts import get_current_site
from .utils import *
from .models import *
from .serializers import *
import jwt
import base64
from django.core.files.base import ContentFile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser
from django.conf import settings
import os

# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
@api_view(['GET'])
def routes(request):
    routes = {
        'routes/': 'api routes',
        'users/': 'list of all users',
        'user/<int:id>/': 'specific user'
    }
    return Response(routes)

@api_view(['GET'])
def users(request):
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def user(request, id):
    user = CustomUser.objects.get(id=id)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def username(request, username):
    user = CustomUser.objects.filter(username=username)
    if (user.exists()):
        return Response({'error': 'Account with this username already exists!'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'data': 'Account with this email does not exist!'})

@api_view(['GET'])
def email_exists(request, email):
    user = CustomUser.objects.filter(email=email)
    if (user.exists()):
        return Response({'error': 'Account with this email already exists!'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'data': 'Account with this email does not exist!'})


@api_view(['POST'])
def signup(request):
    if (CustomUser.objects.filter(username=request.data['username']).exists()):
        return Response({'error': 'Account with this username already exists!'}, status=status.HTTP_400_BAD_REQUEST)
    elif (CustomUser.objects.filter(email=request.data['email']).exists()):
        return Response({'error': 'Account with this email already exists!'},  status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = SignUpSerializer(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
        user = serializer.data
        user_email = CustomUser.objects.get(email=user['email'])
        token = RefreshToken.for_user(user_email).access_token
        current_site = get_current_site(request).domain
        absolute_url = 'http://'+current_site+'/api/email_verify/?token='+str(token)
        email_message = f'Olá {user["username"]},\nFoi feita uma solicitação para verificar seu email e ativar sua nova conta no GoingPlaces.\n' \
                        f'Clique no link abaixo para verificar seu e-mail e ativar sua nova conta:' \
                        f'\n{absolute_url}' \
                        f'\n' \
                        f'\n' \
                        f"Este email é uma surpresa? Por favor, ignore este email e não clique no link acima. Alguém pode ter digitado incorretamente seu endereço de email e acidentalmente tentou adicionar o seu. Neste caso, o seu endereço de email não será adicionado à outra conta."
        data = {'email_subject': 'Verifique o seu endereço email', 'email_message': email_message,
                'from': 'ricardoyosai1610@gmail.com', 'to': str(user['email'])}
        Util.send_mail(data)
        return Response({'user_data': user})

@api_view(['GET'])
def email_verify(request):
    token = request.GET.get('token')
    try:
        payload = jwt.decode(token, options={'verify_signature': False})
        user = CustomUser.objects.get(id=payload['user_id'])
        context = {'user': user}
        if not user.is_verified:
            user.set_password(str(user.password))
            user.is_verified = True
            user.save()
        return render(request, 'api/verified.xhtml', context)
    except jwt.ExpiredSignatureError as Identifier:
        return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.exceptions.DecodeError as Identifier:
        return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def resend(request, id):
    user = CustomUser.objects.get(id=id)
    serializer = UserSerializer(user, many=False)
    token = RefreshToken.for_user(user).access_token
    current_site = get_current_site(request).domain
    absolute_url = 'http://' + current_site + '/api/email_verify/?token=' + str(token)
    email_message = f'Olá {user.username},\nFoi feita uma solicitação para verificar seu email e ativar sua nova conta no GoingPlaces.\n' \
                    f'Clique no link abaixo para verificar seu e-mail e ativar sua nova conta:' \
                    f'\n{absolute_url}' \
                    f'\n' \
                    f'\n' \
                    f"Este email é uma surpresa? Por favor, ignore este email e não clique no link acima. Alguém pode ter digitado incorretamente seu endereço de email e acidentalmente tentou adicionar o seu. Neste caso, o seu endereço de email não será adicionado à outra conta."

    data = {'email_subject': 'Verifique o seu endereço email', 'email_message': email_message,
            'from': 'ricardoyosai1610@gmail.com', 'to': str(user.email)}
    Util.send_mail(data)
    return Response({'user_data': serializer.data})


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_pic(request, id):
    user = CustomUser.objects.get(id=id)
    ext = request.data.get('ext')
    image = request.data.get('profilepic')
    decoded = base64.b64decode(image)
    image_data = ContentFile(decoded, name=f'{user.username}.{ext}')
    user.profilepic = image_data
    image_path = os.path.join(settings.MEDIA_ROOT, f'images/{user.username}.{ext}')
    if os.path.exists(image_path):
        os.remove(image_path)
    user.save()
    return Response({'data': str(user.profilepic)})

@api_view(['POST'])
def edit_user(request, id):
    user = CustomUser.objects.get(id=id)
    serializer = UserSerializer(instance=user, data=request.data)
    if (serializer.is_valid()):
        serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def edit_details1(request, id):
    user = CustomUser.objects.get(id=id)
    token = RefreshToken.for_user(user).access_token
    current_site = get_current_site(request).domain
    absolute_url = 'http://' + current_site + '/api/edit_details2/?token=' + str(token)
    email_message = f'Olá {user.username},\nFoi feita uma solicitação para verificar seu email e mudar alguns detalhes da sua conta no GoingPlaces.\n' \
                    f'Clique no link abaixo para verificar seu e-mail:' \
                    f'\n{absolute_url}' \
                    f'\n' \
                    f'\n' \
                    f"Este email é uma surpresa? Por favor, ignore este email e não clique no link acima. Alguém pode ter digitado incorretamente seu endereço de email e acidentalmente tentou adicionar o seu. Neste caso, o seu endereço de email não será adicionado à outra conta."

    data = {'email_subject': 'Verifique o seu endereço email', 'email_message': email_message,
            'from': 'ricardoyosai1610@gmail.com', 'to': str(request.data['email'])}
    if (request.data['action'] == 'send'):
        Util.send_mail(data)
    return Response({'token': str(token)})

@api_view(['GET'])
def edit_details2(request):
    token = request.GET.get('token')
    try:
        payload = jwt.decode(token, options={'verify_signature': False})
        user = CustomUser.objects.get(id=payload['user_id'])
        context = {'user': user}
        if not user.is_verified1:
            user.is_verified1 = True
            user.save()
        return render(request, 'api/verified2.xhtml', context)
    except jwt.ExpiredSignatureError as Identifier:
        return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.exceptions.DecodeError as Identifier:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def edit_password(request, id):
    user = CustomUser.objects.get(id=id)
    serializer = UserSerializer(data=request.data, instance=user)
    if (serializer.is_valid()):
        serializer.save()
        user.set_password(str(request.data['password']))
        user.save()
    return Response(serializer.data)

@api_view(['GET'])
def email_verify_password1(request, id):
    user = CustomUser.objects.get(id=id)
    token = RefreshToken.for_user(user).access_token
    current_site = get_current_site(request).domain
    absolute_url = 'http://' + current_site + '/api/email_verify_password2/?token=' + str(token)
    email_message = f'Olá {user.username},\nFoi feita uma solicitação para verificar seu email e mudar a senha da sua conta no GoingPlaces.\n' \
                    f'Clique no link abaixo para verificar seu e-mail:' \
                    f'\n{absolute_url}' \
                    f'\n' \
                    f'\n' \
                    f"Este email é uma surpresa? Por favor, ignore este email e não clique no link acima. Alguém pode ter digitado incorretamente seu endereço de email e acidentalmente tentou adicionar o seu. Neste caso, o seu endereço de email não será adicionado à outra conta."

    data = {'email_subject': 'Verifique o seu endereço email', 'email_message': email_message,
            'from': 'ricardoyosai1610@gmail.com', 'to': str(user.email)}
    Util.send_mail(data)
    return Response({'token': str(token)})

@api_view(['GET'])
def email_verify_password2(request):
    token = request.GET.get('token')
    try:
        payload = jwt.decode(token, options={'verify_signature': False})
        user = CustomUser.objects.get(id=payload['user_id'])
        context = {'user': user}
        if not user.is_verified1:
            user.is_verified1 = True
            user.save()
        return render(request, 'api/verified2.xhtml', context)
    except jwt.ExpiredSignatureError as Identifier:
        return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.exceptions.DecodeError as Identifier:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_user(request, id):
    user = CustomUser.objects.get(id=id)
    user.delete()
    return Response({'data': "Object deleted."})

@api_view(['GET'])
def search_user(request, username):
    user = CustomUser.objects.filter(username=username)
    if (user.exists()):
        serializer = UserSerializer(user[0], many=False)
        return Response(serializer.data)
    else:
        return Response({'error': 'Account with this username does not exist!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def cars(request):
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def addCar(request, id):
    user = CustomUser.objects.get(id=id)
    images = request.data.get('images')
    list = []
    for image in images:
        ext = image.get('ext')
        image = image.get('base64')
        decoded = base64.b64decode(image)
        image_data = ContentFile(decoded, name=f'{user.username}.{ext}')
        # serializer = CarImageSerializer(data=image_data)
        # if (serializer.is_valid()):
        #     serializer.save()
        image_instance = CarImage.objects.create(file=image_data)
        list.append(str(image_instance.file))
    info = request.data.get('info')
    info.update({'images': list})
    car = Car.objects.create(user=user, info=info, images=list)
    serializer = CarSerializer(car, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def user_cars(reqeust, id):
    user = CustomUser.objects.get(id=id)
    cars = Car.objects.filter(user=user)
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_license(request, id):
    user = CustomUser.objects.get(id=id)
    images = request.data.get('images')
    list = []
    for image in images:
        ext = image.get('ext')
        image = image.get('base64')
        decoded = base64.b64decode(image)
        image_data = ContentFile(decoded, name=f'{user.username}.{ext}')
        image_instance = Images.objects.create(file=image_data)
        list.append(str(image_instance.file))
    user.drivers_license = True
    user.license_images = list
    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def filter_cars(request):
    cars = Car.objects.order_by(f'-{request.GET.get("q")}', 'user__star')
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def my_trips(request, id):
    trips = MyTrips.objects.filter(client=id)
    serializer = MyTripsSerializer(trips, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def client_trips(request, id):
    trips = MyTrips.objects.filter(car_owner=id)
    serializer = MyTripsSerializer(trips, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_trip(request):
    serializer = MyTripsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def trips(request):
    trips = MyTrips.objects.all()
    serializer = MyTripsSerializer(trips, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_trip_photos(request, id):
    images = request.data.get('images')
    prevImages = request.data.get('prevImages')
    trip = MyTrips.objects.get(id=id)
    list = []
    for image in images:
        ext = image.get('ext')
        image = image.get('base64')
        decoded = base64.b64decode(image)
        image_data = ContentFile(decoded, name=f'{trip.client}{trip.car_owner}.{ext}')
        image_instance = Images.objects.create(file=image_data)
        list.append(str(image_instance.file))
    trip.images = prevImages + list
    trip.save()
    serializer = MyTripsSerializer(trip, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def get_trip(request, id):
    trip = MyTrips.objects.get(id=id)
    serializer = MyTripsSerializer(trip, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_image(request):
    path = request.GET.get('q')
    file = Images.objects.get(file=path)
    file.delete()
    data = request.data
    trip = MyTrips.objects.get(id=data.get('id'))
    trip.images = data.get('images')
    trip.save()
    text = ''
    image_path = os.path.join(settings.MEDIA_ROOT, f'{path}')
    if os.path.exists(image_path):
        os.remove(image_path)
        text = 'Path removed!'
    return Response('Successfully deleted!'+text)

@api_view(['GET'])
def all_images(request):
    images = Images.objects.all()
    serializer = ImagesSerializer(images, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def edit_trip(request, id):
    trip = MyTrips.objects.get(id=id)
    serializer = MyTripsSerializer(instance=trip, data=request.data)
    if (serializer.is_valid()):
        serializer.save()
    return Response(serializer.data)