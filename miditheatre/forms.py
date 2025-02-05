from django import forms
from miditheatre.models import action, settingUser, actionPath, show
from django.utils.safestring import mark_safe

class ActionForm(forms.ModelForm):
    path = forms.ModelChoiceField(
        queryset=actionPath.objects.all(),
        required=False,
        empty_label="/",
        widget=forms.Select(attrs={'class': 'form-text-input'}),
    )
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-text-input'}),
    )
    
    class Meta:
        model = action
        fields = ['name', 'channel', 'key', 'value']
        widgets = {
            'channel': forms.NumberInput(attrs={'min': 0, 'max': 127, 'class': 'form-text-input'}),
            'key': forms.NumberInput(attrs={'min': 0, 'max': 127, 'class': 'form-text-input'}),
            'value': forms.NumberInput(attrs={'min': 0, 'max': 127, 'class': 'form-text-input'}),
        }
class ShowForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-text-input'}),
    )
    description = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-text-input'}),
    )

    class Meta:
        model = show
        fields = ['name', 'description']
class PathForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        queryset=actionPath.objects.all(),
        required=False,
        empty_label="/",
        widget=forms.Select(attrs={'class': 'form-text-input'}), #FORM IS NOT SAVING THIS FIELD
    )
    category = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-text-input'}),
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