from django.urls import path, include

from . import views

urlpatterns = [
    path('login', views.login),
    path('logout', views.logout),
    # admin functions
    path('user', views.UserList.as_view()),

]
