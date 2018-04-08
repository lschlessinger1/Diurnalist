from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^', include('registration.backends.default.urls')),
    url(r'^deactivate/$', views.deactivate, name='deactivate_user'),
]