from django.conf.urls import url
from django.urls import path

from .views import TaskListView, TaskCreateView, CheckCodeView, TestCodeView, \
    TaskDeleteView, GitTakeForm

app_name = "tasks"

urlpatterns = [
    # url(r'^$', TaskListView.as_view(), name='list'),
    url(r'^new$', TaskCreateView.as_view(), name='new'),
    url(r'^check$', CheckCodeView.as_view(), name='check'),
    url(r'^test$', TestCodeView.as_view(), name='test'),
    url(r'^delete$', TaskDeleteView.as_view(), name='delete'),
    url(r'^$', GitTakeForm.as_view(), name='GitTakeForm'),
]
