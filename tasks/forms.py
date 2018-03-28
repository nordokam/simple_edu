from django.forms import ModelForm, Form, CharField

from .models import Task
# from django import forms



class UploadFileForm(ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'file']


class UrlForm(Form):
    # # arg=''
    # def __init__(self, *args, **kwargs):
    #     # if kwargs['arguu']:
    #     #     self.arg = kwargs['arguu']
    #     # super.__init__(self, *args, **kwargs)
    #     super(UrlForm, self).__init__()
    git_url = CharField(label='Ссылка на файл git', max_length=100)