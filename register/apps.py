from django.apps import AppConfig

class registerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'register'

    def ready(self):
        import register.signals  # Import the signals module
