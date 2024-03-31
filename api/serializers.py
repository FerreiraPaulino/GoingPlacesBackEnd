from rest_framework.serializers import ModelSerializer
from .models import *
class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        read_only_fields = ['profilepic']

class SignUpSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'fullname',
                  'username', 'email', 'password', 'phone_number', 'tokens', 'drivers_license', 'license_images']
        read_only_fields = ['id']

class ProfilePicSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['profilepic']

class CarSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

class CarImageSerializer(ModelSerializer):
    class Meta:
        model = CarImage
        fields = '__all__'

class ChatRoomSerializer(ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'

class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class MyTripsSerializer(ModelSerializer):
    class Meta:
        model = MyTrips
        fields = '__all__'

class ImagesSerializer(ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'