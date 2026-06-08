
from django.contrib import admin
from django.urls import path, include
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
