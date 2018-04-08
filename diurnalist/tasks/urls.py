from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^tasks/$', views.TaskListView.as_view(), name='tasks'),
    url(r'^task/(?P<pk>\d+)$', views.TaskDetailView.as_view(), name='task-detail'),
    url(r'^task/create/$', views.TaskCreate.as_view(), name='task_create'),
    url(r'^task/(?P<pk>\d+)/update/$', views.TaskUpdate.as_view(), name='task_update'),
    url(r'^task/(?P<pk>\d+)/delete/$', views.TaskDelete.as_view(), name='task_delete'),
    url(r'^task/(?P<task_id>\d+)/share/$', views.share, name='task_share'),
    url(r'^(?P<task_id>\d+)/mark_done/$', views.mark_done, name='task_done'),
    url(r'^search$', views.TaskSearchListView.as_view(), name='task_search'),
    url(r'^tasks/completed', views.TaskDoneListView.as_view(), name='tasks_completed'),
]