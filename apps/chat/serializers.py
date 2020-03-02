from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message, Thread
from django.core.exceptions import ValidationError


# Thread Serializer
class ThreadCreateSerializer(serializers.ModelSerializer):
    """For Serializing Threads"""

    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    name = serializers.CharField(max_length=50)

    def validate_participants(self, value):
        if len(value) != 2:
            raise ValidationError(message='There can be only two participants')
        return value

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        thread = Thread.objects.create(**validated_data)
        thread.participants.set(participants)
        thread.save()

        return thread

    class Meta:
        model = Thread
        fields = '__all__'


class ThreadDetailSerializer(serializers.ModelSerializer):
    """For Serializing Threads"""

    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()

    class Meta:
        model = Thread
        fields = '__all__'


class ThreadListSerializer(serializers.ModelSerializer):
    """For Serializing Threads"""
    name = serializers.CharField(max_length=50)
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    message = serializers.SerializerMethodField()

    def get_message(self, obj):
        message = obj.message.last()
        if message:
            return message.text


    class Meta:
        model = Thread
        fields = 'participants', 'name', 'created', 'updated', 'message'


class MessageCreateSerializer(serializers.ModelSerializer):
    """For Serializing Messages"""

    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    text = serializers.CharField(max_length=500)
    thread = serializers.PrimaryKeyRelatedField(queryset=Thread.objects.all())
    is_read = serializers.BooleanField(default=False)

    def create(self, validated_data):
        message = Message.objects.create(**validated_data)
        return message

    class Meta:
        model = Message
        fields = '__all__'


class MessageDetailSerializer(serializers.ModelSerializer):
    """For Serializing Messages"""

    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    text = serializers.CharField(max_length=500)
    thread = serializers.PrimaryKeyRelatedField(queryset=Thread.objects.all())
    is_read = serializers.BooleanField(default=False)

    class Meta:
        model = Message
        fields = '__all__'