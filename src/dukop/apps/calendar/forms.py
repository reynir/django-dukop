from django import forms
from django.forms.formsets import formset_factory

from . import models
from .widgets import SplitDateTimeWidget


class EventForm(forms.ModelForm):

    start = forms.DateTimeField(widget=SplitDateTimeWidget())
    end = forms.DateTimeField(widget=SplitDateTimeWidget(), required=False)

    class Meta:
        model = models.Event
        fields = ('name', 'description', 'host', 'venue_name', 'street', 'zip_code', 'city')


class EventTimeForm(forms.ModelForm):

    start = forms.DateTimeField(widget=SplitDateTimeWidget())
    end = forms.DateTimeField(widget=SplitDateTimeWidget())

    class Meta:
        model = models.EventTime
        fields = ('start', 'end')


class EventImageForm(forms.ModelForm):

    is_cover = forms.BooleanField()

    def save(self, commit=True):
        # A very naive implementation of priority, just sets '0' on the
        # cover image
        image = forms.ModelForm.save(self, commit=False)
        if self.cleaned_data['is_cover']:
            image.priority = 0
        else:
            image.priority = 1
        return image

    class Meta:
        model = models.EventImage
        fields = ('image',)


EventTimeFormSet = formset_factory(EventTimeForm, extra=5, max_num=5)
EventImageFormSet = formset_factory(EventImageForm, extra=5, max_num=5)
