from django import template
from ..models import Category ,Article
from django.db.models import Count, Q
from datetime import datetime, timedelta
from django.contrib.contenttypes.models import ContentType
from ..views import post_list



register = template.Library()

@register.simple_tag
def title():
    return "وبلاگ کتاب گیر"


#این قسمت بدرد پنل ادمین میخورد.تعداد پست هایی که منشتر شده را نشان می دهد
@register.simple_tag
def total_posts():
    return Article.published.count()


@register.inclusion_tag("blog/partials/category_navbar.html")
def category_navbar():
    return {
        "category":Category.objects.filter(status="True"),
    }

@register.inclusion_tag("blog/partials/sidebar.html")
def popular_articles():
    last_month = datetime.today()-timedelta(days=30)
    return {
        "articles": Article.objects.published().annotate(count=Count('hits',filter=Q(articlehit__created__gt=last_month))).order_by('count','publish')[:4],
        "title":"مقالات پربازدید ماه"
    }
    
@register.inclusion_tag("blog/partials/slider.html")
def hot_articles():
    content_type_id = user_type = ContentType.objects.get(app_label='blog', model='article').id
    last_month = datetime.today()-timedelta(days=30)
    return {
        "articles": Article.objects.published().annotate(count=Count('comments',filter=Q(comments__posted__gt=last_month) and Q(comments__content_type_id= content_type_id))).order_by('-count','-publish')[:3],
        "title":"مقالات داغ ماه"
    }
    
@register.inclusion_tag("blog/partials/sidebar.html")
def last_articles():
    content_type_id = user_type = ContentType.objects.get(app_label='blog', model='article').id
    last_month = datetime.today()-timedelta(days=30)
    return {
        "articles": Article.objects.published().order_by('-publish')[:3],
        "title":"مقالات اخیر"
    }


@register.inclusion_tag("registration/partials/link.html")
def link(request,link_name,content,classes):
    return {
        "request":request,
        "link_name":link_name,
        "link":"account:{}".format(link_name),
        "content":content,
        "classes":classes,
    }
