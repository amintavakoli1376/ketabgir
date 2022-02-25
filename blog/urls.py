from django.urls import path
from .views import ArticleList , ArticleDetail , CategoryList , AuthorList , ArticlePreview ,SearchList ,LikeView ,AllPosts

app_name = 'blog'
urlpatterns = [
    path('',ArticleList.as_view(), name='home'),
    path('page/<int:page>',ArticleList.as_view(), name='home'),
    path('articles/<slug:slug>', ArticleDetail.as_view() , name='detail'),
    path('preview/<int:pk>', ArticlePreview.as_view() , name='preview'),
    path('category/<slug:slug>', CategoryList.as_view() , name='category'),
    path('category/<slug:slug>/page/<int:page>', CategoryList.as_view() , name='category'),
    path('author/<slug:username>', AuthorList.as_view() , name='author'),
    path('author/<slug:username>/page/<int:page>', AuthorList.as_view() , name='author'),
    path('search/', SearchList.as_view() , name='search'),
    path('search/page/<int:page>', SearchList.as_view() , name='search'),
    path('like/<slug:slug>', LikeView , name='like_post'),
    path('allposts', AllPosts.as_view(), name='posts'),
    
]

