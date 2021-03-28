from django import forms
from . import models

# class MessageForm(forms.Form):
#     your_msg = forms.CharField(label='Your Message', max_length=100)



class ProfileUpdateForm(forms.ModelForm):
    fb_password = forms.CharField(widget=forms.PasswordInput(), max_length=100)
    class Meta:
        model = models.Profile
        fields = ('fb_email', 'fb_password')

### other way 
class TaskCreateForm(forms.ModelForm):
    class Meta:
        
        model = models.Task 
        fields = '__all__'
        #need to add "due date" in fields 
        # fields = ['task_name', 'body', 'user']

# class TaskUpdateForm(forms.ModelForm):
#     class Meta:
        
#         model = models.Task 
#         #need to add "due date" in fields 
#         fields = ['task_name', 'body', 'user']



