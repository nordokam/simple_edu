from django.contrib import admin
from .models import TestCase, Task, TestInOut, Lesson

admin.site.register(TestCase)
admin.site.register(Task)
admin.site.register(Lesson)
admin.site.register(TestInOut)
