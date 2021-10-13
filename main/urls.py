from django.urls import path

from main.views import (
    UserListView
)

urlpatterns = [
    path('', UserListView.as_view(), name='hello'),
]