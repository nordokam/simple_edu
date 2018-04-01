import inspect
from enum import Enum
from django.db import models


class ChoiceEnum(Enum):

    @classmethod
    def choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        # filter down to just properties
        props = [m for m in members if not(m[0][:2] == '__')]
        # format into django choice tuple
        choices = tuple([(str(p[1].value), p[0]) for p in props])
        return choices


class StatusEnum(ChoiceEnum):
    not_tested = 0
    tested = 1
    on_review = 2
    done = 3

class Lesson(models.Model):
    number = models.FloatField(null=True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    # task=models.ForeignKey(Task, verbose_name='Задачи', related_name='tasks',on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=StatusEnum.choices(),
                              default=StatusEnum.not_tested.value)
    lesson=models.ForeignKey(Lesson, verbose_name='Урок', related_name='tasks',on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class TestCase(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(blank=True, null=True)
    task = models.ForeignKey(
        Task, verbose_name='Тесты для задач', related_name='cases',
        on_delete=models.CASCADE)
    def __str__(self):
        return self.title

    def get_items(self):
        return self.items.all()


class TestInOut(models.Model):
    input = models.CharField(max_length=255)
    output = models.CharField(max_length=255)
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE,
                                  verbose_name='Входные/выходные данные',
                                  related_name='items')

    def __str__(self):
        return '{} - {}'.format(self.input, self.output)

