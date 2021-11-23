"""monitoring URL Configuration

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
from django.urls import path, include
from users import views as userViews
from django.contrib.auth import views as authViews
from dadata import views as dadataViews
from app import views as appViews
from excel import views as excelViews
from users.forms import UserOurAuth
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('it_is_ss/', admin.site.urls),
    path('', authViews.LoginView.as_view(template_name='users/auth.html', authentication_form=UserOurAuth), name='auth'),
    path('home/', include('app.urls')),
    path('reg/', userViews.register, name='reg'),
    path('exit/', authViews.LogoutView.as_view(template_name='users/exit.html'), name='exit'),
    path('address/', dadataViews.AddressCreate.as_view(), name='suggest'),
    path('timetable/', appViews.ShowAddressView.as_view(), name='timetable'),
    path('rating/', appViews.ShowRatingView.as_view(), name='rating'),
    path('timetable/<str:username>/', appViews.ShowUserTimetableView.as_view(), name='user-timetable'),
    path('simple_upload/', excelViews.simple_upload, name='simple_upload'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)