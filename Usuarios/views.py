from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views import View
from .forms import UsuarioRegistroForm, UsuarioEditarForm
from .models import Usuario

from django.shortcuts import render

def home_view(request):
    data = {
        'footer': 'true',
    }
    return render(request, 'home/index.html', data)




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

@login_required
def perfil_view(request):
    # Mostrar el perfil del usuario actual
    return render(request, 'Usuarios/perfil.html', {'user': request.user})

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
