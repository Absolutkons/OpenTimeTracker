from django import forms
from django.contrib.auth.models import User

from .models import Project




class AddProjectForm(forms.Form):
    name = forms.CharField(max_length=100,
                            required=True,
                            label='Project: ',
                            widget=forms.TextInput(attrs={'placeholder': 'My Project',
                            }))
    
    rate = forms.IntegerField(required=False,
                            label='Rate: ',
                            widget=forms.NumberInput(attrs={'placeholder': '0',
                            }))