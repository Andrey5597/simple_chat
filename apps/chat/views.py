
from .models import Message, Thread, User
from apps.chat.serializers import ThreadCreateSerializer, ThreadDetailSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ThreadDetailsView(APIView):

    def post(self, request):
        serializer = ThreadCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        participants = request.data['participants']
        existing_thead = Thread.objects.filter(
            participants=User.objects.get(pk=participants[0])).filter(
            participants=User.objects.get(pk=participants[1]))
        if existing_thead:
            output_serializer = ThreadDetailSerializer(existing_thead[0])
            return Response(output_serializer.data, status=status.HTTP_200_OK)
        else:
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, thread_id):
        thread = Thread.objects.get(pk=thread_id)
        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
