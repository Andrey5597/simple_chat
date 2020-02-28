from django.contrib.auth.models import User
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Message, Thread
from .serializers import MessageSerializer, UserSerializer, ThreadSerializer


@csrf_exempt
def user_list(request, pk=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        if pk:                                              # If PrimaryKey (id) of the user is specified in the url
            users = User.objects.filter(id=pk)              # Select only that particular user
        else:
            users = User.objects.all()                      # Else get all user list
        serializer = UserSerializer(users, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)     # Return serialized data
    elif request.method == 'POST':
        data = JSONParser().parse(request)               # On POST, parse the request object to obtain the data in json
        serializer = UserSerializer(data=data)           # Seraialize the data
        if serializer.is_valid():
            serializer.save()                                            # Save it if valid
            return JsonResponse(serializer.data, status=201)     # Return back the data on success
        return JsonResponse(serializer.errors, status=400)     # Return back the errors  if not valid