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




