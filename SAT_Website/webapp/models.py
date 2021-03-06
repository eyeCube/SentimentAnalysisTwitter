from django.db import models


class Email(models.Model):
    name = models.CharField(max_length=100)
    Email = models.CharField(default="placeholder@emai.xyz", primary_key=True, max_length=50)
    EmailSent = models.BooleanField(default=False)
    term_id = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.name


class Tweets(models.Model):
    id = models.IntegerField(primary_key=True)
    text = models.CharField(max_length=768)
    year = models.CharField(max_length=4)

    class Meta:
        managed = False


class Terms(models.Model):
    id = models.IntegerField(primary_key=True)
    term = models.CharField(max_length=356)
    year = models.CharField(max_length=4)
    positivity = models.FloatField()
    sentiment = models.CharField(max_length=20)
    r_tweet = models.TextField()

    class Meta:
        managed = False


class Tags(models.Model):
    id = models.ForeignKey(Tweets, on_delete=models.CASCADE, primary_key=True)
    hashtag = models.CharField(max_length=256)

    class Meta:
        managed = False
