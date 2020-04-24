from .models import *
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from .async_listener import start_listener
from multiprocessing import Process
from .ModelTraining.NuancedSentimentDetection.AnalyzeSentiment import get_sentiment


def home(request):
    return render(request, 'home.html')


def search(request):
    if request.method == 'POST':
        term_id = request.POST['term_id']
        try:
            email = Email.objects.get(Email=request.POST['e'])
            email.EmailSent = False
            email.term_id = term_id
            email.save()
        except Email.DoesNotExist:
            new = Email(name=request.POST['n'], Email=request.POST['e'], term_id=term_id)
            new.save()
        return render(request, 'newemail.html', {'text': "Thanks!"})
    query = request.GET.get('q')
    year = request.GET.get('tweet_year')
    try:
        term = Terms.objects.using('tweets').get(term__exact=query, year=year)
        # tweets = Tweets.objects.using('tweets').all().filter(text__icontains=' ' + query + ' ', year=year)[:10]
        # tweets[0]
    except Terms.DoesNotExist:
        split_query = query.split()

        # listen for tweets in a separate thread to render website for user without delays
        # the process terminates automatically after
        p = Process(target=start_listener, args=split_query)
        p.start()

        new_term = Terms(term=query, year=year)
        new_term.save(using='tweets')
        term_id = Terms.objects.using('tweets').get(term__exact=query, year=year).id
        return render(request, 'newemail.html', {'term_id': term_id})
    return render(request, 'results.html', {'term': term})


def about(request):
    return render(request, 'about.html')


"""
def test(request):
    rows = Tweets.objects.using('tweets').all()
    return render(request, 'tweets.html', {'rows': rows})
"""
