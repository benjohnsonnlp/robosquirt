from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from localflavor.us.forms import USStateField, USStateSelect


class LocationLookupForm(forms.Form):

    state = USStateField(required=True, widget=USStateSelect)
    place = forms.CharField(max_length=25, label="Search for a place (city, county, etc.)")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "location-lookup"
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Find'))