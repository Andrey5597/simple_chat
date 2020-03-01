from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message, Thread
from django.core.exceptions import ValidationError


# Thread Serializer
class ThreadCreateSerializer(serializers.ModelSerializer):
    """For Serializing Threads"""

    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    created = serializers.DateTimeField(required=False)
    updated = serializers.DateTimeField(required=False)

    def validate(self, validated_data):
        if len(validated_data.get('participants')) != 2:
            raise ValidationError(message='There can be only two participants')
        return validated_data

    def create(self, validated_data):
        participants = validated_data.get('participants')
        thread = Thread.objects.create()
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


