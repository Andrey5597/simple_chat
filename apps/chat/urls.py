from django.urls import path
from .views import ThreadDetailsView

urlpatterns = [
    path('threads/', ThreadDetailsView.as_view(), name='Threads'),
    path('threads/<int:thread_id>', ThreadDetailsView.as_view(), name='Threads')

]
