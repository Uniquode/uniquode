from django.urls import path, include

from . import views as main_views


urlpatterns = [
    path('', main_views.HomeView.as_view(), name='home'),
    path('about/', main_views.AboutView.as_view(), name='about'),
    path('contact/', main_views.ContactView.as_view(), name='contact'),
    path('login/', main_views.LoginView.as_view(), name='signin'),
    path('logout/', main_views.LogoutView.as_view(), name='signout'),
    path('articles/', main_views.ArticlesView.as_view(), name='articles'),
    path('news/', main_views.NewsView.as_view(), name='news'),
    path('markdownx/', include('markdownx.urls'))
]
