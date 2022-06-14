from unicodedata import name
from venv import create
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    desription = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    update = models.DateTimeField(auto_now=True)
    create = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-update', '-create']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    create = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]