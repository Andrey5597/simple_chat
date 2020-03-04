from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import (MessageDetailView, MessageReadView, ThreadDetailView,
                    ThreadListView, ThreadMessageListView, UnreadMessageView)

urlpatterns = [
    # method POST(custom) (let us create threads by passing the name and participants(ids) in request)
    # method GET, supports query params ('user_id), in this case queryset will be filtered by user
    path('threads/', ThreadListView.as_view(), name='Threads'),

    # method DELETE (delete thread with specified id)
    path('threads/<int:thread_id>/', ThreadDetailView.as_view(), name='Threads'),

    # method POST (let us create message in specified thread)
    # method GET, let us retrieve all messages in thread
    path('threads/<int:thread_id>/messages/', ThreadMessageListView.as_view(), name='Threads'),

    # method POST (let us create message)
    path('messages/', MessageDetailView.as_view(), name="Thread's messages"),

    # method POST (let us mark messages, as "read")
    path('messages/read/', MessageReadView.as_view(), name="Thread's messages"),

    # method GET (let the authenticated user know how many messages in his threads are unread)
    path('messages/unread/', UnreadMessageView.as_view(), name='Number of unread messages'),

    # method GET for jwt-tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
