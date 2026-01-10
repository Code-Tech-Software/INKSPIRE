from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views import View

from Productos.models import Categoria
from .forms import UsuarioRegistroForm, UsuarioEditarForm, EmailAuthenticationForm
from .models import Usuario

from django.shortcuts import render

def home_view(request):
    categorias = Categoria.objects.filter(visible=True).order_by('nombre')
    data = {
        'footer': True,
        'categorias': categorias,
    }
    return render(request, 'home/index.html', data)



def about(request):
    data = {
        'title': 'Acerca de',
        'subTitle': 'Inicio',
        'subTitle2': 'Acerca de',
        'css': '<link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/>',
        'footer': 'true',
    }
    return render(request, "pages/about.html", data)



def faq(request):
    data = {
        'title': 'Preguntas frecuentes',
        'subTitle': 'Inicio',
        'subTitle2': 'Preguntas frecuentes',
        'css': '<link rel="stylesheet" type="text/css" href="/static/css/variables/variable1.css"/>',
        'footer': 'true',
    }
    return render(request, "pages/faq.html", data)


def contact(request):
    data = {
        'title': 'Contacto',
        'subTitle': 'Inicio',
        'subTitle2': 'Contacto',
        'css': '<link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/>',
        'footer': 'true',
    }
    return render(request, "blog/contact.html", data)


from django.contrib.auth import login, authenticate

class RegistroView(View):
    template_name = 'Usuarios/registro.html'
    form_class = UsuarioRegistroForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # 🔑 Autenticación explícita
            user = authenticate(
                request,
                username=user.username,
                password=form.cleaned_data['password1']
            )

            if user is not None:
                login(request, user)

            return redirect('home')

        return render(request, self.template_name, {'form': form})

class LoginRegistroView(View):
    template_name = 'home/login.html'

    def get(self, request):
        context = {
            'title': 'Acceder',
            'subTitle': 'Inicio',
            'subTitle2': 'Acceder',
            'css': '<link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/>',
        }
        return render(request, self.template_name, context)

    def post(self, request):
        context = {
            'title': 'Acceso',
            'subTitle': 'Inicio',
            'subTitle2': 'Acceso',
            'css': '<link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/>',
            'data': request.POST,  # para no perder lo escrito
        }

        if 'login_submit' in request.POST:
            login_form = EmailAuthenticationForm(request, data=request.POST)

            if login_form.is_valid():
                login(request, login_form.get_user())
                return redirect('home')
            else:
                context['login_errors'] = login_form.non_field_errors()

        elif 'registro_submit' in request.POST:
            registro_form = UsuarioRegistroForm(request.POST, request.FILES)

            if registro_form.is_valid():
                user = registro_form.save()
                user = authenticate(
                    request,
                    username=user.username,
                    password=registro_form.cleaned_data['password1']
                )
                if user:
                    login(request, user)
                return redirect('home')
            else:
                context['registro_errors'] = registro_form.errors

        return render(request, self.template_name, context)
@login_required
def perfil_view(request):
    # Mostrar el perfil del usuario actual
    return render(request, 'Usuarios/perfil.html', {'user': request.user})



@login_required
def account(request):
    data = {
        'title': 'Cuenta',
        'subTitle': 'Inicio',
        'subTitle2': 'Cuenta',
        'css': '<link rel="stylesheet" type="text/css" href="/static/css/variables/variable6.css"/>',
        'footer': 'true',
        'script': '<script src="/static/js/vendors/zoom.js"></script>',
    }
    return render(request, "shop/account.html", data)


@login_required
def editar_perfil_view(request):
    user = request.user
    if request.method == 'POST':
        form = UsuarioEditarForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = UsuarioEditarForm(instance=user)
    return render(request, 'Usuarios/editar_perfil.html', {'form': form})
