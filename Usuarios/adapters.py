from allauth.account.adapter import DefaultAccountAdapter
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAccountAdapter(DefaultAccountAdapter):

    def populate_username(self, request, user):
        """
        Genera un username único automáticamente
        """
        base_username = slugify(user.email.split('@')[0])
        username = base_username
        counter = 1

        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user.username = username
