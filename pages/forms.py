from django import forms
from . import models
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# class MessageForm(forms.Form):
#     your_msg = forms.CharField(label='Your Message', max_length=100)

class BootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({'class': 'form-control'})

class ProfileUpdateForm(BootstrapForm):
    fb_password = forms.CharField(widget=forms.PasswordInput(), max_length=100, label="Facebook Password")
    class Meta:
        model = models.Profile
        fields = ('fb_email', 'fb_password')

### other way 
class TaskCreateForm(BootstrapForm):
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

class BootstrapLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({'class': 'form-control'})

class BootstrapSignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapSignupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({'class': 'form-control'})

class TaskForm(BootstrapForm):
    CUSTOM_HANDLED_FIELDS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    class Meta:
        model = models.Task
        fields = [
            'task_name',
            'body',
            'start_date',
            'end_date',
            'Sunday',
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'time_of_day',
            'friend_name'
        ]
