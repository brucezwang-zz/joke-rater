from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Author(models.Model):
    category_id = models.AutoField(primary_key=True, default=0)
    name = models.CharField(max_length=100)

    @classmethod
    def create(cls, name):
        author = cls(name=name)
        return author

    def __unicode__(self):
        return self.title

class Joke(models.Model):
    category_id = models.AutoField(primary_key=True, default=0)
    text = models.TextField(max_length=3000)
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    def averageRating(self):
        reviews = self.review_set.all()
        b = 0
        n = 0
        for review in reviews:
            b += review.rating
            n += 1

        try:
            return b / n
        except:
            return 0

    def __unicode__(self):
        return self.title

class Review(models.Model):
    category_id = models.AutoField(primary_key=True, default=0)
    rating = models.PositiveSmallIntegerField(default=5, validators=[MaxValueValidator(100), MinValueValidator(1)])
    comments = models.TextField(max_length=3000)
    joke = models.ForeignKey(Joke, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    def __unicode__(self):
        return self.title
