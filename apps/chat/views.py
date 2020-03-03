
from .models import Message, Thread, User
from apps.chat.serializers import (ThreadSerializer,
                                   # ThreadDetailSerializer,
                                   ThreadListSerializer,
                                   MessageCreateSerializer,
                                   MessageDetailSerializer,
                                   MessageCountSerializer
                                   )
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated


class ThreadListView(generics.ListCreateAPIView):
    serializer_class = ThreadSerializer

    def get_queryset(self):
        queryset = Thread.objects.all()
        if 'user_id' in self.request.query_params:
            queryset = queryset.filter(participants__id=self.request.query_params['user_id'])
        return queryset

    @staticmethod
    def get_thread(participants):
        try:
            return Thread.objects.filter(
                participants__in=participants
            )
        except Thread.DoesNotExist:
            return None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        thread = self.get_thread(serializer.validated_data['participants'])
        if thread is not None:
            return Response(ThreadSerializer(thread).data, status=status.HTTP_200_OK)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ThreadDetailView(generics.RetrieveDestroyAPIView):
    lookup_url_kwarg = 'thread_id'
    serializer_class = ThreadSerializer
    queryset = Thread.objects.all()


class ThreadMessageListView(generics.ListCreateAPIView):
    serializer_class = MessageDetailSerializer

    def get_queryset(self):
        return Message.objects.filter(thread=self.kwargs['thread_id'])


class MessageDetailView(generics.CreateAPIView):
    serializer_class = MessageCreateSerializer


class MessageListView(generics.ListAPIView):
    serializer_class = MessageDetailSerializer

    def get_queryset(self):
        return Message.objects.filter(thread_id=self.kwargs['thread_id'])


class MessageReadView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if 'messages' in request.data and isinstance(request.data['messages'], list):
            Message.objects.filter(id__in=request.data['messages']).update(is_read=True)
            return Response(status=status.HTTP_200_OK)
        return Response({'messages': 'Invalid format.'}, status=status.HTTP_400_BAD_REQUEST)


class UnreadMessageView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Thread.objects.all()
    serializer_class = MessageCountSerializer








