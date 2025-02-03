from django import forms
from miditheatre.models import action

class ActionForm(forms.ModelForm):
    class Meta:
        model = action
        fields = ['name', 'channel', 'key', 'value']
        widgets = {
            'channel': forms.NumberInput(attrs={'min': 0, 'max': 127}),
            'key': forms.NumberInput(attrs={'min': 0, 'max': 127}),
            'value': forms.NumberInput(attrs={'min': 0, 'max': 127}),
        }