from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('admin/', admin.site.urls),
    path('sign-up', views.signup, name='Sign-up'),
    path('sign-in', views.signin, name='signin'),
    # path(r'^ginfo/(?P<user_hash>\w+)/$', views.authWelcome, name='auth-wel'),
    path('ginfo', views.authWelcome, name='auth-wel'),
    path('failinfo', views.failInformation, name='fail-info'),
    

    path('dum', views.dum, name='Dum'),
    path('get-image', views.getImage, name='Dum'),
    path('check-auth', views.checkAuth, name='checkAuth'),
    path('check-user', views.checkUser, name='checkUser'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)