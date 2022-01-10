from os import name
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.deletion import PROTECT

fs = FileSystemStorage('/media/tb')

class Timetable(models.Model):
    name = models.CharField(max_length=100, unique=True)
    #file = models.FileField(storage=fs)
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Groups(models.Model):
    name = models.CharField(max_length=20, unique=True)
    tb = models.ForeignKey('Timetable', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    # def Meta:
    #     orde


class Profile(models.Model):
    external_id = models.PositiveIntegerField(verbose_name='Внешний ID пользователя', unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'#{self.external_id} {self.name}'


class Message(models.Model):
    profile = models.ForeignKey(Profile, on_delete=PROTECT)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Сообщение {self.text} от {self.profile}'

class File(models.Model):
    name = models.CharField(max_length=100, unique=True)
    file = models.FileField(upload_to='media/tb', unique=True)

    def __str__(self):
        return self.name