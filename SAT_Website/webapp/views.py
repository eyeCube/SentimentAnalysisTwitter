from .models import Email
from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404


def home(request):
    return render(request, 'search.html')


def search(request):
    if request.method == 'POST':
        new = Email(name=request.POST['n'], Email=request.POST['e'])
        new.save()
        return render(request, 'newemail.html', {'text': "Thanks!", 'isPost': True})
    query = request.GET.get('q')
    try:
        email = Email.objects.get(Email=query)
    except Email.DoesNotExist:
        return render(request, 'newemail.html')
    return render(request, 'results.html', {'email': email})
