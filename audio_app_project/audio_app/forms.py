# forms.py
from django import forms

class AudioRecordingForm(forms.Form):
    audio_file = forms.FileField()
    # Add any other fields you want to include in the form
