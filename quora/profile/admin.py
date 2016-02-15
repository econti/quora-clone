from django.contrib import admin
from django.apps import apps

profile = apps.get_app_config('profile')

for model_name, model in profile.models.items():
    admin.site.register(model)
