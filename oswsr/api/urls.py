from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'work-shift', views.WorkShiftViewSet)

urlpatterns = [
    path('login', views.login),
    path('logout', views.logout),
    # admin functions
    path('user', views.UserList.as_view()),
    path('', include(router.urls))
]
