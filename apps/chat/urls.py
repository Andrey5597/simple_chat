from django.urls import path
from .views import (ThreadDetailView,
                    ThreadListView,
                    MessageDetailView,
                    ThreadMessageListView,
                    MessageReadView,
                    UnreadMessageView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # methods POST(custom) GET, supports query params ('user_id), in this case queryset will be filtered by users
    path('threads/', ThreadListView.as_view(), name='Threads'),
    # method POST(custom), if
    path('threads/<int:thread_id>/', ThreadDetailView.as_view(), name='Threads'),                # method  DELETE
    path('threads/<int:thread_id>/messages/', ThreadMessageListView.as_view(), name='Threads'),
    path('messages/<int:message_id>/', MessageDetailView.as_view(), name="Thread's messages"),
    path('messages/read/', MessageReadView.as_view(), name="Thread's messages"),
    path('messages/unread', UnreadMessageView.as_view(), name='Number of unread messages'),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
