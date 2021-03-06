from django.contrib import messages
from django.views.generic import ListView, DetailView
from account.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from account.mixins import AuthorAccessMixin
from django.http import HttpResponseRedirect
from .models import Article, Category
from django.db.models import Q
from django.urls import reverse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from pathlib import Path
from .models import NewsletterUser, Newsletter, Contact
from .forms import NewsletterUserSignUpForm, NewsletterCreationForm
from django.utils.html import strip_tags
from taggit.models import Tag


# Create your views here.

def LikeView(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article.likes.add(request.user)
    return HttpResponseRedirect(reverse('blog:detail', args=[str(article.slug)]))


class ArticleList(ListView):
    queryset = Article.objects.published()
    paginate_by = 9


class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article.objects.published(), slug=slug)

        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all():
            article.hits.add(ip_address)

        return article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stuff = get_object_or_404(Article, slug=self.kwargs['slug'])
        total_likes = stuff.total_likes()
        context["total_likes"] = total_likes
        return context


class ArticlePreview(AuthorAccessMixin, DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)


# class CategoryList(ListView):
#     paginate_by = 9
#     template_name = "blog/category_list.html"

#     def get_queryset(self):
#         global category
#         slug = self.kwargs.get('slug')
#         category = get_object_or_404(Category.objects.active(), slug=slug)
#         return category.articles.published()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["category"] = category
#         return context

def category(request, slug=None):
    context = {
        "category": get_object_or_404(Category, slug=slug, status=True)
    }
    return render(request, "blog/category_list.html", context)


# class AuthorList(ListView):
#     paginate_by = 9
#     template_name = "blog/author_list.html"

#     def get_queryset(self):
#         global author
#         username = self.kwargs.get('username')
#         author = get_object_or_404(User, username=username)
#         return author.articles.published()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["author"] = author
#         return context

def author(request, username=None):
    context = {
        "author": get_object_or_404(User, username=username)
    }
    return render(request, "blog/author_list.html", context)


class SearchList(ListView):
    paginate_by = 9
    template_name = "blog/search_list.html"

    def get_queryset(self):
        search = self.request.GET.get('q')
        return Article.objects.filter(Q(description__icontains=search) | Q(title__icontains=search))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get('q')
        return context


def post_list(request, tag_slug=None):
    post_list = Article.objects.all()
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 9)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        "items": items,
        "page_range": page_range,
    }
    template = 'blog/all_posts.html'
    return render(request, template, context)


def newsletter_signup(request):
    form = NewsletterUserSignUpForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            messages.warning(request, '?????? ?????????? ???????? ???????? ?????? ??????',
                             "alert alert-warning alert-dismissible")
        else:
            instance.save()
            messages.success(request, '?????????? ???? ???????????? ?????? ????',
                             "alert alert-success alert-dismissible")

            subject = "???????? ???? ???????????? ??????"
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email]
            sbd = str(Path(settings.BASE_DIR))
            with open(sbd + "/templates/newsletters/sign_up_email.txt")as f:
                signup_message = f.read()
            message = EmailMultiAlternatives(
                subject=subject, body=signup_message, from_email=from_email, to=to_email)
            html_template = get_template(
                "newsletters/sign_up_email.html").render()
            message.attach_alternative(html_template, "text/html")
            message.send()

    context = {
        'form': form,
    }
    template = "blog/list.html"
    return render(request, template, context)


def newsletter_unsubscribe(request):
    form = NewsletterUserSignUpForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        if NewsletterUser.objects.filter(email=instance.email).exists():
            NewsletterUser.objects.filter(email=instance.email).delete()
            messages.success(request, '???????????? ?????? ?????? ????',
                             "alert alert-success alert-dismissible")

            subject = "?????? ???????????? ?????????? ???????? ??????"
            from_email = settings.EMAIL_HOST_USER
            to_email = [instance.email]
            sbd = str(Path(settings.BASE_DIR))
            with open(sbd + "/templates/newsletters/unsubscribe_email.txt")as f:
                signup_message = f.read()
            message = EmailMultiAlternatives(
                subject=subject, body=signup_message, from_email=from_email, to=to_email)
            html_template = get_template(
                "newsletters/unsubscribe_email.html").render()
            message.attach_alternative(html_template, "text/html")
            message.send()
        else:
            messages.warning(request, '?????? ?????????? ???????? ?????? ???????? ??????',
                             "alert alert-warning alert-dismissible")

    context = {
        'form': form,
    }
    template = "newsletters/unsubscribe.html"
    return render(request, template, context)


def control_newsletter(request):
    form = NewsletterCreationForm(request.POST or None)
    if form.is_valid():
        instance = form.save()
        newsletter = Newsletter.objects.get(id=instance.id)
        if newsletter.status == "published":
            subject = newsletter.subject
            body = strip_tags(newsletter.body)
            from_email = settings.EMAIL_HOST_USER
            for email in newsletter.email.all():
                send_mail(subject=subject, message=body, from_email=from_email, recipient_list=[
                          email], fail_silently=True)

        return redirect('account:control_newsletter_list')
    context = {
        "form": form,
    }
    template = 'registration/control_newsletter.html'
    return render(request, template, context)


def control_newsletter_list(request):
    newsletters = Newsletter.objects.all()
    paginator = Paginator(newsletters, 10)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        "items": items,
        "page_range": page_range,
    }
    template = 'registration/control_newsletter_list.html'
    return render(request, template, context)


def control_newsletter_edit(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == 'POST':
        form = NewsletterCreationForm(request.POST, instance=newsletter)
        if form.is_valid():
            newsletter = form.save()
            if newsletter.status == "published":
                subject = newsletter.subject
                body = strip_tags(newsletter.body)
                from_email = settings.EMAIL_HOST_USER
                for email in newsletter.email.all():
                    send_mail(subject=subject, message=body, from_email=from_email, recipient_list=[
                              email], fail_silently=True)
            return redirect('account:control_newsletter_list')

    else:
        form = NewsletterCreationForm(instance=newsletter)
    context = {
        "form": form,
    }
    template = 'registration/control_newsletter.html'
    return render(request, template, context)


def control_newsletter_delete(request, pk):
    newsletter = get_object_or_404(Newsletter, pk=pk)
    if request.method == 'POST':
        form = NewsletterCreationForm(request.POST, instance=newsletter)
        if form.is_valid():
            newsletter.delete()
            return redirect('account:control_newsletter_list')

    else:
        form = NewsletterCreationForm(instance=newsletter)
    context = {
        "form": form,
    }
    template = 'registration/control_newsletter_delete.html'
    return render(request, template, context)


def contact(request):
    if request.method == "POST":
        contact = Contact()
        message_name = request.POST.get('message-name')
        message_email = request.POST.get('message-email')
        message = request.POST.get('message')
        contact.message_name = message_name
        contact.message_email = message_email
        contact.message = message
        contact.save()

        return render(request, 'blog/contact.html', {'message_name': message_name})

    else:
        return render(request, 'blog/contact.html', {})


def control_contact_list(request):
    contact = Contact.objects.all()
    paginator = Paginator(contact, 10)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    index = items.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 5 if index >= 5 else 0
    end_index = index + 5 if index <= max_index - 5 else max_index
    page_range = paginator.page_range[start_index:end_index]

    context = {
        "items": items,
        "page_range": page_range,
    }
    template = 'registration/control_contact_list.html'
    return render(request, template, context)
