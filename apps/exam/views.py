from django.shortcuts import render, redirect
from models import User, Quote
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def index(request):

    return render(request, 'exam/index.html')

def register(request):
    if request.method == "POST":
        user = User.objects.register(request.POST)
        if 'errors' in user:
            for error in user['errors']:
                messages.error(request, error)
            return redirect('/')
        if 'theuser' in user:
            request.session['theuser'] = user['theuser']
            request.session['userid'] = user['userid']
            return redirect('/quotes')

def login(request):
    if request.method == "POST":
        user = User.objects.login(request.POST)
        if 'errors' in user:
            for error in user['errors']:
                messages.error(request, error)
                return redirect('/')
        if 'theuser' in user:
            request.session['theuser'] = user['theuser']
            request.session['userid'] = user['userid']
            return redirect('/quotes')

def logout(request):
    del request.session['theuser']
    del request.session['userid']
    return redirect('/')

def quotes(request):
    all_quotes = Quote.objects.exclude(favorite=request.session['userid'])
    favorite_quotes = Quote.objects.filter(favorite=request.session['userid'])
    context={
    'all' : all_quotes,
    'fav' : favorite_quotes
    }
    return render(request, 'exam/quotes.html', context)

def addquote(request):
    if request.method =='POST':
        quote = Quote.objects.add(request.POST, request.session['userid'])
        if 'errors' in quote:
            for error in quote['errors']:
                messages.error(request, error)
                redirect ('/quotes')
    return redirect('/quotes')

def favorite(request, id):
    this_quote= Quote.objects.get(id=id)
    favorite = User.objects.get(id=request.session['userid'])
    this_quote.favorite.add(favorite)
    this_quote.save()
    return redirect('/quotes')

def unfavorite(request, id):
    this_quote= Quote.objects.get(id=id)
    favorite = User.objects.get(id=request.session['userid'])
    this_quote.favorite.remove(favorite)
    this_quote.save()
    return redirect('/quotes')

def user(request, id):
    my_quotes= Quote.objects.filter(posted__id=id)
    context={
    'quote' :my_quotes,
    'user' :User.objects.get(id=id),
    'count' :Quote.objects.annotate(qcount=Count('quote')).filter(posted__id=id)
    }
    return render(request, 'exam/user.html', context)
