from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.ProfilePage.as_view(), name='profile_main_page'),
]