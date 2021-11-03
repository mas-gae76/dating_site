from rest_framework.generics import CreateAPIView
from .serializers import CreationSerializer
from rest_framework.permissions import IsAuthenticated


class RegisterView(CreateAPIView):
    serializer_class = CreationSerializer

    def perform_create(self, serializer):
        serializer.save()
