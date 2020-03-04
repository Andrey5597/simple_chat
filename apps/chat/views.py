
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination

from apps.chat.serializers import (MessageCountSerializer,
                                   MessageCreateSerializer,
                                   MessageDetailSerializer, ThreadSerializer)

from .models import Message, Thread


class ThreadListView(generics.ListCreateAPIView):
    serializer_class = ThreadSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = Thread.objects.all()
        if 'user_id' in self.request.query_params:
            queryset = queryset.filter(participants__id=self.request.query_params['user_id'])
        return queryset

    @staticmethod
    def get_thread(participants):
        threads = Thread.objects.filter(participants=participants[0]
                                        ).filter(participants=participants[1])
        if threads.exists():
            return threads.last()
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
    pagination_class = LimitOffsetPagination


class ThreadMessageListView(generics.ListCreateAPIView):
    serializer_class = MessageDetailSerializer
    pagination_class = LimitOffsetPagination

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


class UnreadMessageView(APIView):

    def get(self, request):
        user_threads_ids = self.request.user.threads.all().values_list('id', flat=True)
        unread_messages = Message.objects.filter(thread_id__in=user_threads_ids,
                                                 is_read=False).exclude(sender=self.request.user)
        output_serializer = MessageCountSerializer(unread_messages)

        return Response(output_serializer.data, status=status.HTTP_200_OK)
