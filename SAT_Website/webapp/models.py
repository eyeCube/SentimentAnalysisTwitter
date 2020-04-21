from django.db import models


class Email(models.Model):
    name = models.CharField(max_length=100)
    Email = models.CharField(default="placeholder@emai.xyz", primary_key=True, max_length=50)
    EmailSent = models.BooleanField(default=False)
    tweet_id = models.IntegerField(null=True, default=None)

    def __str__(self):
        return self.name


class Tweets(models.Model):
    id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=768)
    year = models.CharField(max_length=4)

    class Meta:
        managed = False


class Tags(models.Model):
    id = models.ForeignKey(Tweets, on_delete=models.CASCADE, primary_key=True)
    text = models.CharField(max_length=256)

    class Meta:
        managed = False
