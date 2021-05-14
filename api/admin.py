from django.contrib import admin
from .models import Gadget, Category, Comment, Order, DeliveryAddress
# Register your models here.

admin.site.register(Gadget)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Order)
admin.site.register(DeliveryAddress)
