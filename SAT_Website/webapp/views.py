from .models import *
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from .async_listener import start_listener
from multiprocessing import Process


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
    year = request.GET.get('tweet_year')
    try:
        tweets = Tweets.objects.using('tweets').all().filter(text__icontains=' ' + query + ' ', year=year)[:10]
        tweets[0]
    except IndexError:
        query = query.split()

        # listen for tweets in a separate thread to render website for user without delays
        # the process terminates automatically after
        p = Process(target=start_listener, args=query)
        p.start()

        # new_tweet = Tweets(text=query, year=2020)
        # new_tweet.save(using='tweets')
        # tweet_id = (Tweets.objects.using('tweets').get(text__exact=query, year=2020)).id
        tweet_id = 1
        return render(request, 'newemail.html', {'tweet_id': tweet_id})
    return render(request, 'results.html', {'tweets': tweets})


def about(request):
    return render(request, 'about.html')


"""
def test(request):
    rows = Tweets.objects.using('tweets').all()
    return render(request, 'tweets.html', {'rows': rows})
"""
