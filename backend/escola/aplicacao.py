from django.apps import AppConfig
from importlib import import_module


class EscolaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'escola'
    verbose_name = 'Gestão Escolar'

    def import_models(self):
        self.models = self.apps.all_models[self.label]
        self.models_module = import_module(f'{self.name}.modelos')

