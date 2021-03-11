from typing import List, Optional, OrderedDict

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Message, Thread


class ThreadSerializer(serializers.ModelSerializer):
    """Serializer for creating and displaying Threads."""
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = (
            'id',
            'participants',
            'name',
            'created',
            'updated',
            'last_message',
        )

    def validate_participants(self, objs: List[User]) -> List[User]:
        if len(objs) != 2:
            raise ValidationError(message='There can be only two participants')
        return objs

    def get_last_message(self, obj: Thread) -> Optional[str]:
        message = obj.messages.last()
        return message.text if message else None

    def create(self, validated_data: dict) -> Thread:
        participants = validated_data.pop('participants')
        thread = super().create(validated_data)
        thread.participants.add(*participants)
        return thread


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for creating and displaying messages."""
    class Meta:
        model = Message
        fields = '__all__'


class MessageCountSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    number_of_unread_messages = serializers.SerializerMethodField()

    def get_number_of_unread_messages(self, obj: OrderedDict) -> int:
        user = obj.get('user')
        user_threads_ids = user.threads.values_list('id', flat=True)
        return Message.objects.filter(
            thread_id__in=user_threads_ids, is_read=False
        ).exclude(sender=user).count()
