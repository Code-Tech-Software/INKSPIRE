from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import EmailAuthenticationForm
urlpatterns = [
    # Registro y perfil
    path('', views.home_view, name='home'),
    path('registro/', views.RegistroView.as_view(), name='registro'),
    path('perfil/', views.perfil_view, name='perfil'),
    path('perfil/editar/', views.editar_perfil_view, name='editar_perfil'),

    # Login / Logout usando vistas incorporadas
    path('login/',auth_views.LoginView.as_view(template_name='registration/login.html',authentication_form=EmailAuthenticationForm),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Cambio de contraseña
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html',
                                               success_url='/password_change/done/'),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),
]
