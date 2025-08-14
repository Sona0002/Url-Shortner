from django import forms

class ShortenForm(forms.Form):
    url = forms.URLField(
        label="Long URL",
        help_text="Paste the full URL you want to shorten.",
        widget=forms.URLInput(attrs={
            'placeholder': 'https://example.com/very/long/link',
            'class': 'form-control'
        })
    )