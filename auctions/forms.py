from django import forms
from django.forms import ModelForm, Textarea, NumberInput, URLField

from .models import Listing

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'description', 'starting_bid', 'category', 'image',)
        widgets = {
            'description': Textarea (attrs={'cols':80, 'rows':4}),
            'starting_bid': NumberInput(attrs={'width':12}),
        }

