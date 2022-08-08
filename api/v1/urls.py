from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from django.views.generic import TemplateView
from .viewsets import product, user

router = DefaultRouter()
router.register(
    r'products', 
    product.ProductViewSet, 
    basename='products'
)

router.register(
    r'users', 
    user.UserViewSet, 
    basename='users'
)

urlpatterns = [
    path('web-auth/', include('rest_framework.urls')),
    path('docs/', include_docs_urls(title='ZebrandsAPI', public=False))    
] + router.urls
