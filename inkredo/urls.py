"""inkredo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from server.views.company import create_company_endpoint, handle_company_endpoint
from server.views.users import create_user_endpoint, handle_user_endpoint
from server.views.accounts import handle_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('company/', create_company_endpoint),
    path('company/<int:company_id>', handle_company_endpoint),
    path('user/', create_user_endpoint),
    path('user/<int:user_id>', handle_user_endpoint),
    path('login', handle_login),
]
