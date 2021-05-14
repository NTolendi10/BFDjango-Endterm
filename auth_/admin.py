from django.contrib import admin
from .models import User, Seller, Profile
# Register your models here.
admin.site.register(User)
admin.site.register(Seller)
admin.site.register(Profile)
