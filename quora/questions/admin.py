from django.contrib import admin
from django.apps import apps

questions = apps.get_app_config('questions')

for model_name, model in questions.models.items():
    admin.site.register(model)
