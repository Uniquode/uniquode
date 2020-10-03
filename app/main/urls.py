from django.urls import path

from . import views as main_views


urlpatterns = [
    path('', main_views.HomeView.as_view(), name='home'),
    path('about/', main_views.AboutView.as_view(), name='about')
]
