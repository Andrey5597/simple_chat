from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message, Thread


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    """For Serializing User"""
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']


# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    """For Serializing Message"""
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    thread = serializers.SlugRelatedField(many=False, slug_field='thread', queryset=Thread.objects.all())

    class Meta:
        model = Message
        fields = '__all__'


# Thread Serializer
class ThreadSerializer(serializers.ModelSerializer):
    """For Serializing Threads"""
    participant = serializers.SlugRelatedField(many=True, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Thread
        fields = '__all__'
