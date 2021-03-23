
from django.contrib import admin
from django.urls import path, include
from blog import views
from knitting import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', views.index, name='home'),
    path('', views.MoviesList.as_view(), name='home'),
    # path('page/<int:pk>/', views.post, name='page'),
    path('page/<int:pk>/', views.MovieDetailView.as_view(), name='page'),
    path('about/', views.about, name='about'),
    # path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),
    path('summernote/', include('django_summernote.urls')),
    path('profile/', views.profile, name='profile'),
    path('registration/', views.register, name='register')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
