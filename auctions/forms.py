from .models import *
from django import forms
from django.core.exceptions import ValidationError


class CreateListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        starting_bid = cleaned_data.get('starting_bid')

        if not title:
            raise ValidationError('Title is required')

        if not starting_bid:
            raise ValidationError('Starting bid is required')

        return cleaned_data
