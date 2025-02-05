from django import forms
from miditheatre.extras.logger import LOGGER
from miditheatre.models import action, settingUser, actionPath, show
from django.utils.safestring import mark_safe

class ActionForm(forms.ModelForm):
    """ModelForm for the action model."""
    
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
        """Meta class for ActionForm model configuration."""
        model = action
        fields = ['name', 'channel', 'key', 'value', 'path']
        widgets = {
            'channel': forms.NumberInput(attrs={'min': 0, 'max': 127, 'class': 'form-text-input'}),
            'key': forms.NumberInput(attrs={'min': 0, 'max': 127, 'class': 'form-text-input'}),
            'value': forms.NumberInput(attrs={'min': 0, 'max': 127, 'class': 'form-text-input'}),
        }
        
    def save(self, commit=True):
        """Override save to include the path field."""
        instance = super().save(commit=False)
        for path_mod in actionPath.objects.all():
            if path_mod.__str__ == self.cleaned_data.get('path'):
                instance.path = path_mod
        LOGGER.info("Path: %s", instance.path)
        if commit:
            instance.save()
        return instance
    
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
    def save(self, commit=True):
        """Override save to include the path field."""
        instance = super().save(commit=False)
        for show_mod in show.objects.all():
            if show_mod.__str__ == self.cleaned_data.get('show_current'):
                instance.show_current = show_mod
        LOGGER.info("Path: %s", instance.show_current)
        if commit:
            instance.save()
        return instance 