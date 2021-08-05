from django.urls import path, include

urlpatterns = [
    path('api-cafe/', include('api.urls')),
]
