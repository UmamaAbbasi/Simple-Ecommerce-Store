from django.apps import AppConfig
from django.db.utils import OperationalError

class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'

    def ready(self):
        try:
            from django.contrib.auth.models import User  # import inside ready()
            admin_user, created = User.objects.get_or_create(username='Umama')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            if created:
                admin_user.set_password('admin123')  # change to secure password
            admin_user.save()
        except OperationalError:
            # This will happen during `migrate` before the auth tables exist
            pass
