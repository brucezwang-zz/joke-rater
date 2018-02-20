from django.shortcuts import render
from engine.models import Joke, Review, Author
from django.db.models.functions import Length
from .forms import ReviewForm, JokeForm

def homePage(request):
    return render(request, 'engine/templates/home.html')

def thanksPage(request):
    return render(request, 'engine/templates/thanks.html')

def nothanksPage(request):
    return render(request, 'engine/templates/nothanks.html')

def showJokesByField(request, field="title"):
    if field == "rating" :
        jokes = Joke.objects.all()
        jokes = sorted(jokes, key = lambda t: t.averageRating())
    else:
        if field == "author" :
            field = "author__name"

        try:
            jokes = Joke.objects.all().order_by(field)
        except:
            jokes = Joke.objects.all().order_by("title")


    return render(request, 'engine/templates/jokes.html', {'jokes':jokes})

def showAuthorsByField(request, field="name"):
    if field == "contribs" :
        authors = Author.objects.annotate(contriblen = (Length('joke_set') + Length('article_set'))).order_by('contriblen')
    else:
        try:
            authors = Author.objects.all().order_by(field)
        except:
            authors = Author.objects.all().order_by("name")

    return render(request, 'engine/templates/authors.html', {'authors':authors, })

def newJoke(request):
    if request.method == 'POST':
        form = JokeForm(request.POST)
        if form.is_valid():
            query = Author.objects.filter(name__iexact=form.cleaned_data['name'])
            if not query.exists():
                author = Author.objects.create(name=form.cleaned_data['name'])
                author.save()
            else:
                author = query.first()

            joke = Joke(title=form.cleaned_data['title'], text=form.cleaned_data['text'])
            author.joke_set.add(joke)

            return HttpResponseRedirect('/thanks/')

        else:
            return HttpResponseRedirect('/nothanks/')

    else:
        form = JokeForm()

    return render(request, 'engine/templates/newjoke.html', {'form': form})

def newReview(request, jokeid):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        try:
            joke = Joke.objects.filter(category_id__iexact=jokeid).first()
        except:
            return HttpResponseRedirect('/nothanks/')

        if form.is_valid():
            query = Author.objects.filter(name__iexact=form.cleaned_data['name'])
            if not query.exists():
                author = Author(name=form.cleaned_data['name'])
                author.save()
            else:
                author = query.first()

            review = Review(rating=form.cleaned_data['rating'], comments=form.cleaned_data['text'])
            author.review_set.add(review)
            joke.review_set.add(review)

            return HttpResponseRedirect('/thanks/')

        else:
            return HttpResponseRedirect('/nothanks/')

    else:
        form = ReviewForm()

    return render(request, 'engine/templates/newreview.html', {'form': form, 'range': range(1,11)})
