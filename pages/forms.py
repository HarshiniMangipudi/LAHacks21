from django import forms

class MessageForm(forms.Form):
    your_msg = forms.CharField(label='Your Message', max_length=100)
