from django import forms
from django.forms import ModelForm, Textarea, NumberInput, URLField

from . import util

from .models import Listing, Bid

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'description', 'starting_bid', 'category', 'image',)
        widgets = {
            'description': Textarea (attrs={'cols':80, 'rows':4}),
            'starting_bid': NumberInput(attrs={'width':12}),
        }

class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['title_id', 'bid_amount']

        labels = {
            "bid_amount": "Your Bid",
        }
        widgets = {
            'title_id': forms.HiddenInput(),
            'bid_amount': forms.NumberInput(),
        }

    def clean_bid_amount(self):
        cleaned_data = self.cleaned_data.get('bid_amount')
        max_bid = util.get_bid_details(self.initial['title_id'])['max_bid']
        if (max_bid == None):
            max_bid = cleaned_data['title_id'].starting_bid
        if ((cleaned_data < (max_bid + 1))):
            raise forms.ValidationError("Bid Amount does not confirm to Auction Rules. Retry")
        return cleaned_data
