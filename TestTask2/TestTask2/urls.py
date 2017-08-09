"""TestTask2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from ref.views import login_user, logout_user, register, generate_referal, top10, tables

urlpatterns = [
    url(r'^$', login_user, name='login'),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^gen_ref/$', generate_referal, name='gen_ref'),
    url(r'^top/$', top10, name='top'),
    url(r'^tables/$', tables, name='tables'),

]
