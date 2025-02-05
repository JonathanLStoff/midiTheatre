from django import forms
from miditheatre.models import action, settingUser, actionPath, show

class ActionForm(forms.ModelForm):
    path = forms.ModelChoiceField(
        queryset=actionPath.objects.all(),
        required=False,
        empty_label="/"
    )
    
    class Meta:
        model = action
        fields = ['name', 'channel', 'key', 'value']
        widgets = {
            'channel': forms.NumberInput(attrs={'min': 0, 'max': 127}),
            'key': forms.NumberInput(attrs={'min': 0, 'max': 127}),
            'value': forms.NumberInput(attrs={'min': 0, 'max': 127}),
        }
class PathForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        queryset=actionPath.objects.all(),
        required=False,
        empty_label="/",
    )
    category = forms.CharField(
        max_length=255,
        help_text="Category name"
    )
    class Meta:
        model = actionPath
        fields = ['category', 'parent']
        
class SettingsForm(forms.ModelForm):
    THEME_CHOICES = [
        ('light', 'Light Mode'),
        ('dark', 'Dark Mode'),
    ]
    show_current = forms.ModelChoiceField(
        queryset=show.objects.all(),
        required=False,
        empty_label="None",
        help_text="Loaded Show"
    )
    theme = forms.ChoiceField(
        choices=THEME_CHOICES,
        widget=forms.RadioSelect
    )
    go_key = forms.IntegerField(
        min_value=1,
        max_value=256,
        help_text="Keycode for 'Go' action"
    )
    stop_key = forms.IntegerField(
        min_value=1,
        max_value=256,
        help_text="Keycode for 'Stop' action"
    )

    class Meta:
        model = settingUser
        fields = ['theme', 'go_key', 'stop_key', 'show_current']  # Update fields to match template
        widgets = {
            'go_key': forms.NumberInput(attrs={'class': 'form-control'}),
            'stop_key': forms.NumberInput(attrs={'class': 'form-control'}),
        }    