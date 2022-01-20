from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from .serializers import CreationSerializer, SympathySerializer
from .models import User, Sympathy, UserFilter
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django_filters import rest_framework as filters
from django.db.models.functions import *
from django.db.models import F


class RegisterView(CreateAPIView):
    serializer_class = CreationSerializer

    def perform_create(self, serializer):
        serializer.save()


class MatchingView(RetrieveUpdateAPIView):
    serializer_class = SympathySerializer

    def get_queryset(self):
        return Sympathy.objects.filter(id=self.kwargs.get('pk', None))

    def get(self, request, *args, **kwargs):
        try:
            match_user = User.objects.get(id=self.kwargs.get('pk', None))
            current_user = request.user
            matching = self.check_sympathy(current_user, match_user)
            serializer = SympathySerializer(matching)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            return Response({'Ошибка': 'Этого пользователя нет на сайте знакомств'}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({'Ошибка': 'Вы уже оценивали этого пользователя'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'Ошибка': 'Возникли проблемы на стороне сервера'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def check_sympathy(cur_user, match_user):
        existing1 = Sympathy.objects.filter(who=cur_user, whom=match_user)
        existing2 = Sympathy.objects.filter(who=match_user, whom=cur_user)
        if existing1 and existing2:
            existing1.update(matching=True)
            existing2.update(matching=True)
            MatchingView.send_email(cur_user, match_user)
            MatchingView.send_email(match_user, cur_user)
            return existing1
        return Sympathy.objects.create(who=cur_user, whom=match_user)

    @staticmethod
    def send_email(user1, user2):
        subject = 'Сайт знакомств'
        message = f'Вы понравились {user2.first_name}! Почта участника: {user2.email}'
        admin_email = settings.EMAIL_HOST_USER
        user_email = [user1.email]
        return send_mail(subject, message, admin_email, user_email)


class DistanceFilter(filters.DjangoFilterBackend):

    def filter_queryset(self, request, queryset, view):
        selected_users = User.objects.exclude(id=request.user.id)
        distance = request.GET.get('distance')
        first_name = request.GET.get('first_name')
        last_name = request.GET.get('last_name')
        gender = request.GET.get('gender')
        if first_name or last_name or gender:
            selected_users = selected_users.filter(first_name__icontains=first_name, last_name__icontains=last_name,
                                                   gender__icontains=gender)
        if distance:
            radius = 6371
            cur_user_longitude = Radians(request.user.longitude)
            cur_user_latitude = Radians(request.user.latitude)
            selected_users = selected_users.annotate(
                distance=radius * ACos(
                    Sin(Radians(F('latitude')))
                    *
                    Sin(cur_user_latitude)
                    +
                    Cos(Radians(F('latitude')))
                    *
                    Cos(cur_user_latitude)
                    *
                    Cos(cur_user_longitude -
                        Radians(F('longitude'))
                        )
                )
            ).filter(distance__lte=distance).order_by('distance')
        return selected_users


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = CreationSerializer
    filter_backends = (DistanceFilter,)
    filterset_class = UserFilter
