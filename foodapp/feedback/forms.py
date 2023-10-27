from django import forms
from .models import Restaurant, Review
    
class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content']

    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}))