from django.db import models
from django.conf import settings

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=70)
    email = models.EmailField()
    phone = models.CharField(max_length=14)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    userCreator = models.ForeignKey(settings.AUTH_USER_MODEL)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return self.name