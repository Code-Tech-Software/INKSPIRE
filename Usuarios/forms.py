from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario


class UsuarioRegistroForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('email', 'first_name', 'last_name', 'telefono', 'url_imagen')

    def save(self, commit=True):
        user = super().save(commit=False)

        # 🔑 username automático usando el email
        base_username = self.cleaned_data['email'].split('@')[0]
        username = base_username
        counter = 1

        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user.username = username
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user

class UsuarioEditarForm(UserChangeForm):
    password = None  # ocultar campo password en el form de edición (opcional)
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name',  'telefono', 'url_imagen')



# Usuarios/forms.py
from django import forms
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    error_messages = {
        'invalid_login': 'Correo o contraseña incorrectos.',
        'inactive': 'Esta cuenta está inactiva.'
    }

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get('email')
        password = cleaned.get('password')

        if email and password:
            try:
                user_obj = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                raise forms.ValidationError(self.error_messages['invalid_login'], code='invalid_login')

            # authenticate espera username; le pasamos el username del usuario encontrado
            user = authenticate(self.request, username=user_obj.username, password=password)

            if user is None:
                raise forms.ValidationError(self.error_messages['invalid_login'], code='invalid_login')
            if not user.is_active:
                raise forms.ValidationError(self.error_messages['inactive'], code='inactive')

            self.user_cache = user

        return cleaned

    def get_user(self):
        return self.user_cache
