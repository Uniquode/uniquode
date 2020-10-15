from django.conf import settings
from django.urls import path, include
from django.views.static import serve

from . import views as main_views


urlpatterns = [
    path('', main_views.HomeView.as_view(), name='home'),
    path('about/', main_views.AboutView.as_view(), name='about'),
    path('contact/', main_views.MessagesView.as_view(), name='contact'),
    path('login/', main_views.LoginView.as_view(), name='signin'),
    path('logout/', main_views.LogoutView.as_view(), name='signout'),
    path('articles/', main_views.ArticlesView.as_view(), name='articles'),
    path('news/', main_views.NewsView.as_view(), name='news'),
    path('links/', main_views.LinksView.as_view(), name='news'),
    path('test/', main_views.TestView.as_view(), name='test'),
    path('markdownx/', include('markdownx.urls')),
    path('media/<path:path>', serve, {'document_root':settings.MEDIA_ROOT})
]
