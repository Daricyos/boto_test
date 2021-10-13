from django.shortcuts import render # noqa
from django.views.generic.list import ListView

from .models import Users

class UserListView(ListView):
    template_name = 'users_list.html'
    model = Users
