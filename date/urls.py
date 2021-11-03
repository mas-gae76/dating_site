from django.urls import path, include
from .views import *

urlpatterns = [
    path('clients/create/', RegisterView.as_view(), name='create'),
    path('', include('rest_framework.urls')),
]
