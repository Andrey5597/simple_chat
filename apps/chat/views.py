
from .models import Message, Thread, User
from apps.chat.serializers import ThreadCreateSerializer, ThreadDetailSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics


class ThreadDetailsView(APIView):

    def post(self, request):
        serializer = ThreadCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        participants = request.data['participants']
        existing_thread = Thread.objects.filter(
            participants=User.objects.get(pk=participants[0])).filter(
            participants=User.objects.get(pk=participants[1]))
        if existing_thread:
            output_serializer = ThreadDetailSerializer(existing_thread[0])
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, thread_id):
        thread = Thread.objects.get(pk=thread_id)
        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ThreadsListView(generics.ListAPIView):

    serializer_class = ThreadDetailSerializer

    def get_queryset(self):
        participant = self.kwargs['participant_id']
        return Thread.objects.filter(participants__id=participant)
