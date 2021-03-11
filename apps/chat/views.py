from typing import List, Optional

from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Message, Thread
from .serializers import (MessageCountSerializer,
                          MessageSerializer,
                          ThreadSerializer)


class ThreadListView(generics.ListCreateAPIView):
    serializer_class = ThreadSerializer

    def get_queryset(self):
        queryset = Thread.objects.all()
        filter_dict = {}
        user_id = self.request.query_params.get('user_id')
        if user_id:
            filter_dict.update(participants__id=user_id)
        return queryset.filter(**filter_dict)

    @staticmethod
    def get_thread(participants: List[User]) -> Optional[Thread]:
        if len(participants) == 2:
            user_1, user_2 = participants
            thread = Thread.objects.filter(
                participants=user_1
            ).filter(participants=user_2).last()
            return thread if thread else None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ThreadDetailView(generics.RetrieveDestroyAPIView):
    lookup_url_kwarg = 'thread_id'
    serializer_class = ThreadSerializer
    queryset = Thread.objects.all()


class ThreadMessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(thread=self.kwargs['thread_id'])


class MessageDetailView(generics.CreateAPIView):
    serializer_class = MessageSerializer


class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        return Message.objects.filter(thread_id=self.kwargs.get('thread_id'))


class MessageReadView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if 'messages' in request.data and isinstance(request.data, dict):
            if isinstance(request.data.get('messages'), list):
                Message.objects.filter(id__in=request.data['messages']).update(is_read=True)
            return Response(status=status.HTTP_200_OK)
        return Response({'messages': 'Invalid format.'}, status=status.HTTP_400_BAD_REQUEST)


class UnreadMessageView(generics.RetrieveAPIView):
    serializer_class = MessageCountSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data={'user': request.user.id})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
