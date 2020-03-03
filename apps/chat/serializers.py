from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message, Thread
from django.core.exceptions import ValidationError


# Thread Serializer
class ThreadSerializer(serializers.ModelSerializer):
    """For Serializing Threads"""

    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    last_message = serializers.SerializerMethodField()

    def validate_participants(self, value):
        if len(value) != 2:
            raise ValidationError(message='There can be only two participants')
        return value

    def get_last_message(self, obj):
        message = obj.messages.last()
        if message:
            return message.text

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        thread = Thread.objects.create(**validated_data)
        thread.participants.set(participants)
        thread.save()

        return thread

    class Meta:
        model = Thread
        fields = ('participants', 'name', 'created', 'updated', 'last_message', 'id')
        read_only_fields = ('last_message', )


class ThreadListSerializer(serializers.ModelSerializer):
    """For Serializing Threads"""
    last_message = serializers.SerializerMethodField()

    def get_last_message(self, obj):
        message = obj.messages.last()
        if message:
            return message.text

    class Meta:
        model = Thread
        fields = ('participants', 'name', 'created', 'updated', 'last_message')


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

    class Meta:
        model = Message
        fields = '__all__'


class MessageCountSerializer(serializers.ModelSerializer):

    number_of_unread_messages = serializers.SerializerMethodField()

    def get_number_of_unread_messages(self, obj):
        queryset_1 = obj.objects.fitter(participants=self.request.user)
        number_of_unread_messages = Message.objects.filter(pa)




    class Meta:
        model = Message
        fields = ('number_of_unread_messages', )

