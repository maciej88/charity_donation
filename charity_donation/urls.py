"""charity_donation URL Configuration

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
from django.contrib.auth.decorators import login_required
from django.urls import path
from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', UserLogin.as_view(), name='login'),
    path('logout/',  login_required(UserLogout.as_view()), name='logout'),
    path('register/', UserAdd.as_view(), name='register'),
    path('', MainPage.as_view(), name='main'),
    path('add-donation/',  login_required(AddDonation.as_view()), name='donation'),
    path('confirmation/',  login_required(ConfirmationView.as_view()), name='confirmation'),
    path('user/<int:user_id>/', UserDetails.as_view(), name='user-details'),
    path('user/edit/',  login_required(UserUpdate.as_view()), name='user-update'),
    path('get_institution_by_category/', get_institution_by_category, name='get_institution_by_category'),
    path('rest/', InstitutionList.as_view()),
    path('rest/<int:pk>', InstitutionView.as_view()),
]
