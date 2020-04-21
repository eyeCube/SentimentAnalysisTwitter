from .models import *
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404


def home(request):
    return render(request, 'home.html')


def search(request):
    if request.method == 'POST':
        tweet_id = request.POST['tweet_id']
        try:
            email = Email.objects.get(Email=request.POST['e'])
            email.EmailSent = False
            email.tweet_id = tweet_id
            email.save()
        except Email.DoesNotExist:
            new = Email(name=request.POST['n'], Email=request.POST['e'], tweet_id=tweet_id)
            new.save()
        return render(request, 'newemail.html', {'text': "Thanks!"})
    query = request.GET.get('q')
    try:
        tweets = Tweets.objects.using('tweets').filter(text__icontains=query)
        tweets[0]
    except IndexError:
        # insert whatever tweepy must do here
        # note: query contains the text  being looked for by user
        new_tweet = Tweets(text=query, year=2020)
        new_tweet.save(using='tweets')
        tweet_id = (Tweets.objects.using('tweets').get(text__exact=query, year__exact=2020)).id
        return render(request, 'newemail.html', {'tweet_id': tweet_id})
    email = Email.objects.get(Email='andre@guiraud.biz')
    return render(request, 'results.html', {'email': email})


def about(request):
    return render(request, 'about.html')


def test(request):
    rows = Tweets.objects.using('tweets').all()
    return render(request, 'tweets.html', {'rows': rows})
