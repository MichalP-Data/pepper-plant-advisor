from django import forms


class MessageForm(forms.Form):
    content = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ask about growing hot peppers...'}),
        max_length=2000,
        required=True
    )

