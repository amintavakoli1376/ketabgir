from django.urls import path
from .views import newsletter_signup,newsletter_unsubscribe

urlpatterns = [
    path('sign_up', newsletter_signup , name='newsletter_signup'),
    path('unsubscribe', newsletter_unsubscribe , name='newsletter_unsubscribe'),
]