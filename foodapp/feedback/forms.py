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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = '' 