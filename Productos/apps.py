from django.apps import AppConfig

class ProductosConfig(AppConfig):
    name = 'Productos'

    def ready(self):
        import Productos.signals
