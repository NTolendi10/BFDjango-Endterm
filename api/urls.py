from django.urls import path
from rest_framework import routers

from .views import OrdersViewSet, category_products, ProductsView, CommentView, ProfileViewSet, CategoryView

router = routers.SimpleRouter()
router.register('products', ProductsView)
router.register('myorders', OrdersViewSet)
router.register('basket', ProfileViewSet)

urlpatterns = [
    path('product/<int:pk>/comments/', CommentView.as_view()),
    path('categories/', CategoryView.as_view()),
    path('category/<int:pk>/', category_products),
]

urlpatterns += router.urls
