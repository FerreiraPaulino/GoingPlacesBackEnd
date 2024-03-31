from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Car)
admin.site.register(CarImage)
admin.site.register(Images)
admin.site.register(ChatRoom)
admin.site.register(Message),
admin.site.register(MyTrips)