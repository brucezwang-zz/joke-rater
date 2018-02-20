from django.contrib import admin
from .models import Joke, Author, Review

class allAdmin(admin.ModelAdmin):
    pass

# Register your models here.
admin.site.register(Joke, allAdmin)
admin.site.register(Author, allAdmin)
admin.site.register(Review, allAdmin)
