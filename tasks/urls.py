from django.conf.urls import url

from .views import Index, TestFileFromGitHub, get_file_from_pc, TestFileFromPC

app_name = "tasks"


urlpatterns = [
    url(r'^$', Index.as_view(), name='Index'),
    url(r'^file_from_github$', TestFileFromGitHub.as_view(), name='GitHubTakeFile'),
    url(r'^file_from_pc$', TestFileFromPC.as_view(), name='home'),

]
