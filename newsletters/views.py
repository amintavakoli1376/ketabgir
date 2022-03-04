from django.shortcuts import render
from .models import  NewsletterUser
from .forms import NewsletterUserSignUpForm

# Create your views here.

def newsletter_signup(request):
    form = NewsletterUserSignUpForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            print("این ایمیل قبلا وارد شده است")
        else:
            instance.save()
    
    context = {
        'form':form,
    }
    template = "newsletters/sign_up.html"
    return render(request, template, context)


def newsletter_unsubscribe(request):
    form = NewsletterUserSignUpForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            NewsletterUser.objects.filter(email=instance.email).delete()
        else:
            print("ایمیلی به این آدرس وجود ندارد")
            
    context = {
        'form':form,
    }
    template = "newsletters/unsubscribe.html"
    return render(request, template, context)