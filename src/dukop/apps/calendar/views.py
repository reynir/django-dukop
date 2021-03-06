from django.shortcuts import render
from django.views.generic.edit import CreateView

from . import forms
from . import models


def index(request):
    return render(request, "calendar/index.html")


class EventCreate(CreateView):

    template_name = 'calendar/event/create.html'
    model = models.Event
    form_class = forms.EventForm

    def get(self, request, *args, **kwargs):
        """Handle GET requests: instantiate a blank version of the form."""
        self.object = None
        self.images_form = forms.EventImageFormSet(prefix='images')
        self.times_form = forms.EventTimeFormSet(prefix='times')
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = None
        self.images_form = forms.EventImageFormSet(data=request.POST, prefix='images')
        self.times_form = forms.EventTimeFormSet(data=request.POST, prefix='times')
        form = self.get_form()
        if form.is_valid() and self.images_form.is_valid() and self.times_form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return CreateView.form_valid(self, form)

    def form_invalid(self, form):
        return CreateView.form_valid(self, form)

    def get_context_data(self, **kwargs):
        c = CreateView.get_context_data(self, **kwargs)
        c['times'] = self.times_form
        c['images'] = self.images_form
        return c
