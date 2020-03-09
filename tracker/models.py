from django.db import models
from users.models import User


class Client(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(to=User,
                             on_delete=models.CASCADE,
                             related_name='clients')


class WorkInterval(models.Model):
    user = models.ForeignKey(to=User,
                             on_delete=models.CASCADE,
                             related_name='intervals')
    client = models.ForeignKey(to=Client,
                               on_delete=models.CASCADE,
                               related_name='intervals')
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
