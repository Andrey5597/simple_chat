from django.urls import path
from .views import ThreadDetailsView, ThreadsListView, MessageDetailView, MessageListView

urlpatterns = [
    path('threads/', ThreadDetailsView.as_view(), name='Threads'),
    path('threads/<int:thread_id>', ThreadDetailsView.as_view(), name='Threads'),
    path('threads/participant/<int:participant_id>', ThreadsListView.as_view()
         , name="Participant's_threads "),
    path('thread/messages/', MessageDetailView.as_view(), name='Messages'),
    path('thread/messages/<int:thread_id>', MessageListView.as_view(), name="Thread's messages")

]
