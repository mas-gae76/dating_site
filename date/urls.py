from django.urls import path, include
from .views import *

urlpatterns = [
    path('clients/create/', RegisterView.as_view(), name='create'),
    path('clients/<int:pk>/match/', MatchingView.as_view(), name='match'),
    path('', include('rest_framework.urls')),
]
