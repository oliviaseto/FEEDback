from django import forms
from .models import Restaurant, Review
    
class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', "street_address", "city", "state", "zip_code"]

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = ''

class AdminMessageForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['admin_message']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['admin_message'].label = ''