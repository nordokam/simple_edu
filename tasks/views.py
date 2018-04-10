
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, View
from django.http import HttpResponseRedirect, JsonResponse

from .models import Task
from .forms import UploadFileForm
from .utils import check_code, test_code

#
from .forms import  GitHubTakeFileForm
import os
import requests
import base64
from .models import Lesson

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage


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

class Index(View):
    def get(self, request):
        lessons = Lesson.objects.all()
        tasks = Task.objects.all()
        for task in tasks:
            print(task.title)
        form = GitHubTakeFileForm()
        return render(request, 'tasks/git_take_url.html',
                      {'form': form, 'lessons':lessons, 'tasks':tasks})

def get_file_from_pc(file_for_upload, name_for_save=''):
    fs = FileSystemStorage()
    if not name_for_save:
        name_for_save = file_for_upload.name
    file_path = fs.save(name_for_save, file_for_upload)
    uploaded_file_url = fs.url(file_path)
    return uploaded_file_url

def get_file_from_git_hub(git_hub_link):
    if git_hub_link.find('github.com') >= 0:
        # Преобразование простой ссылки в api-ссылку
        git_hub_api_link = git_hub_link.replace('blob/master', 'contents') \
            .replace('https://github.com', 'https://api.github.com/repos')
        file_response = requests.get(git_hub_api_link)
        file_bytes = base64.b64decode(file_response.json()['content'])
        file = open('media/file_for_test.py', 'w')
        file.write(file_bytes.decode('utf-8'))
        file.close()
    else:
        return 'Not git hub file link'


def testing_income_file(file_path, file_name, task_id):
    errors, check_errors, test_errors = [], [], []
    check_errors, check_valid = check_code(file_path)
    test_errors, test_valid = test_code(task_id, file_path, file_name)
    all_err = errors + check_errors + test_errors
    return all_err


class TestFileFromPC(View):
    def post(self, request):
        file_path = 'media/file_for_test.py'
        file_name = 'file_for_test.py'
        task_id = request.POST['task_i']
        if os.path.exists(file_path):
            os.remove(file_path)
        file_for_upload = request.FILES['myfile']
        uploaded_file_url = get_file_from_pc(file_for_upload, 'file_for_test.py')
        testing_file_err = testing_income_file(uploaded_file_url, file_name, task_id)
        if len(testing_file_err) > 0:
            os.remove(file_path)
            return JsonResponse({'errors': testing_file_err, 'valid': False})

        os.remove(file_path)
        return JsonResponse({'errors': 'no errors', 'valid': True})


class TestFileFromGitHub(View):
    def post(self, request, *args, **kwargs):

        form = GitHubTakeFileForm(request.POST)
        if form.is_valid():
            file_path = 'media/file_for_test.py'
            file_name = 'file_for_test.py'
            task_id = request.POST['task_id']
            incum_link = str(request.POST['git_url'])

            taking_file_err = get_file_from_git_hub(incum_link)
            if taking_file_err:
                return JsonResponse({'errors': taking_file_err, 'valid': False})

            testing_file_err = testing_income_file(file_path, file_name, task_id)
            if len(testing_file_err) > 0:
                os.remove(file_path)
                return  JsonResponse({'errors':testing_file_err, 'valid':False})

            os.remove(file_path)
            return JsonResponse({'errors':'no errors', 'valid':True})
        else:
            return JsonResponse(
                {'errors': 'Not git hub file link', 'valid': False})






