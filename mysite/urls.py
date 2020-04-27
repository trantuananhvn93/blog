"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from django.conf.urls import url
from blog.views import chatbot, chatbotReply, ner, nerReply, HomeView, post_detail

from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('chatbot', chatbot, name='chatbot'),
    path('chatbotReply', chatbotReply, name='chatbotReply'),
    path('ner', ner, name='ner'),
    path('nerReply', nerReply, name='nerReply'),
    # path('home', homepage, name='homePage'),
    path('', HomeView.as_view(), name='home'),
    # path('post-<int:pk>/', PostDetailView.as_view(), name='post'),
    path('post-<int:post_id>/', post_detail, name='post'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)