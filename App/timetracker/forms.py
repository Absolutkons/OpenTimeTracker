from django import forms
from django.contrib.auth.models import User

from .models import Project




class AddProjectForm(forms.Form):
    name = forms.CharField(max_length=100,
                            required=True,
                            label='Project Name: ',
                            widget=forms.TextInput(attrs={'placeholder': 'Project Name',
                            }))
    
    rate = forms.IntegerField(required=False,
                            label='Hourly Rate: ',
                            widget=forms.NumberInput(attrs={'placeholder': 'Hourly Rate',
                            }))
    
    def __init__(self, *args, **kwargs):
        super(AddProjectForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'