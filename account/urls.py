from django.contrib.auth import views
from django.urls import path
from blog.views import control_newsletter, control_newsletter_list, control_newsletter_edit, control_newsletter_delete
from .views import (ArticleList , ArticleCreate , ArticleUpdate ,
                    ArticleDelete ,Profile)

app_name = 'account'

urlpatterns = [
    path('',ArticleList.as_view(),name='home'),
    path('article/create',ArticleCreate.as_view(),name='article-create'),
    path('article/update/<int:pk>',ArticleUpdate.as_view(),name='article-update'),
    path('article/delete/<int:pk>',ArticleDelete.as_view(),name='article-delete'),
    path('profile/',Profile.as_view(),name='profile'),
    path('newsletter/',control_newsletter,name='control_newsletter'),
    path('newsletter-list/',control_newsletter_list,name='control_newsletter_list'),
    path('newsletter-edit/<int:pk>', control_newsletter_edit, name='control_newsletter_edit'),
    path('newsletter-delete/<int:pk>', control_newsletter_delete, name='control_newsletter_delete'),
]