from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from .views import UserRegisterView, SellerRegisterView, ProfileUpdate
urlpatterns = [
    path('login/', obtain_jwt_token),
    path('signup/', UserRegisterView.as_view()),
    path('seller_me/', SellerRegisterView.as_view()),
    path('profile/', ProfileUpdate.as_view({'put': 'put', 'delete': 'delete'})),
]
