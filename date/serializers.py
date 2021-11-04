from rest_framework import serializers
from .models import User, Sympathy


class CreationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('avatar', 'first_name', 'last_name', 'gender', 'email', 'password')

    def create(self, validated_data):
        user = User(email=validated_data['email'],
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],
                    avatar=validated_data['avatar'],
                    gender=validated_data['gender'])
        user.set_password(validated_data['password'])
        user.save()

        return user


class SympathySerializer(serializers.ModelSerializer):

    class Meta:
        model = Sympathy
        extra_kwargs = {'who': {'read_only': True}, 'matching': {'read_only': True}}
        fields = ('who', 'whom', 'matching')
