from django.db import models


class Email(models.Model):
    name = models.CharField(max_length=100)
    Email = models.CharField(default="placeholder@emai.xyz", primary_key=True, max_length=50)
    EmailSent = models.BooleanField(default=False)

    def __str__(self):
        return self.name
