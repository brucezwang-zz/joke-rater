from django import forms

class JokeForm(forms.Form):
    name = forms.CharField(label='Author Name', max_length=100)
    title = forms.CharField(label='Joke Title', max_length=100)
    text = forms.CharField(label='Text', max_length=3000, widget=forms.Textarea)

class ReviewForm(forms.Form):
    name = forms.CharField(label='Author Name', max_length=100)
    text = forms.CharField(label='Text', max_length=3000, widget=forms.Textarea)
    rating = forms.IntegerField(label='Rating (1-10)')
