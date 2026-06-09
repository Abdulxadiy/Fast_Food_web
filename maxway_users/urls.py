from django.urls import path
from .views import *


urlpatterns = [
    path('', home_page, name='home_page'),
    path('order/', order_page, name='order_page'),
]