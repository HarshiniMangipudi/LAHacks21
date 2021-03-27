from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import MessageForm
from .utils import send_msg

def homePageView(request):
    return HttpResponse('Hello, World!')

def sentView(request):
    return HttpResponse('Sent!')

# def simpleForm(request):
#     # return HttpResponse('Hello, World!')
#     return render(request, 'pages/simpleForm.html')

def simpleForm(request):
    # return HttpResponse('Hello, World!')
    # return render(request, 'pages/simpleForm.html')
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = MessageForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            msg = form.cleaned_data['your_msg']
            send_msg(msg)
            print(f"success! sent: {msg}")

            return HttpResponseRedirect('/sent')
        print("invalid form!")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = MessageForm()

    return render(request, 'simpleForm.html', {'form': form})


