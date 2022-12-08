from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
import django.utils

# Create your models here.
class Topic(models.Model):
    title = models.CharField(
        max_length=100, help_text='Entre o Título', unique=True, verbose_name='Título')
    description = models.TextField(
        help_text='Entre a Descrição', verbose_name='Descrição')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    date = models.DateTimeField(
        default=django.utils.timezone.now
    )
    tags = TaggableManager()   

    def __str__(self):
        return self.title