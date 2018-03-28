from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, View
from django.http import HttpResponseRedirect, JsonResponse

from .models import Task
from .forms import UploadFileForm
from .utils import check_code, test_code

#
from .forms import  UrlForm
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
import os
import requests
import base64
from .models import Lesson

class TaskCreateView(FormView):
    form_class = UploadFileForm
    template_name = 'tasks/task_new.html'
    success_url = reverse_lazy('tasks:list')

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('tasks:list'))
        else:
            return self.form_invalid(form)


class TaskListView(ListView):
    model = Task


class CheckCodeView(View):

    def post(self, request, *args, **kwargs):
        task_id = request.POST['task_id']
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            errors = []
            valid = False
        else:
            errors, valid = check_code(task.file.path)
        return JsonResponse(
            {'errors': errors, 'valid': valid})


class TestCodeView(View):

    def post(self, request, *args, **kwargs):
        task_id = request.POST['task_id']
        errors, valid = test_code(task_id)
        return JsonResponse({'errors': errors, 'valid': valid})


class TaskDeleteView(View):

    def post(self, request, *args, **kwargs):
        task_id = request.POST['task_id']
        Task.objects.filter(id=task_id).delete()
        return JsonResponse({'errors': [], 'valid': True})

class GitTakeForm(View):
    def get(self, request):
        lessons = Lesson.objects.all()
        tasks = Task.objects.all()
        for task in tasks:
            print(task.title)
        form = UrlForm()
        return render(request, 'tasks/git_take_url.html',
                      {'form': form, 'lessons':lessons, 'tasks':tasks})

    def post(self, request, *args, **kwargs):
        errors, check_errors, test_errors = [],[],[]
        valid, check_valid, test_valid = True, True, True
        form = UrlForm(request.POST)
        # submit = request.POST['your_name']
        # print(submit)
        if form.is_valid():
            if request.POST['git_url'].find('github.com') >=0:
                def get_api_link(git_url):
                    git_api_url = git_url.replace('blob/master', 'contents')\
                        .replace('https://github.com','https://api.github.com/repos')
                    return git_api_url
                github_api_file_url = get_api_link(request.POST['git_url'])
                file_response = requests.get(github_api_file_url)
                file_bytes = base64.b64decode(file_response.json()['content'])
                print(file_bytes.decode('utf-8'))
                file = open('media/file_for_test.py', 'w')
                file.write(file_bytes.decode('utf-8'))
                file.close()
                # task_for_test = Task(title='file_for_test', file='file_for_test.py')
                current_task_id = request.POST['task_id']
                try:
                    current_task = Task.objects.get(pk=current_task_id)
                except Task.DoesNotExist:
                    errors = ['Task does not exist']
                    valid = False
                else:
                    current_task.file='file_for_test.py'
                    current_task.save()
                    check_errors, check_valid = check_code(current_task.file.path)
                    test_errors, test_valid = test_code(current_task.id)
                    current_task.file = ''
                    current_task.save()
                return JsonResponse(
                    {'errors': errors + check_errors + test_errors,
                     'valid': valid and check_valid and test_valid})

            else:
                return JsonResponse(
                    {'errors':'Not git hub file link', 'valid': False})

