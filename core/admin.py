from django.contrib import admin
from django.apps import apps

# FIXME: This is not the best practice for registering models in
#  the Django admin. Automatically registering all models may expose
#  models that should remain hidden or uneditable. It's better to
#  explicitly register only the necessary models with custom admin
#  configurations if needed.
app_models = apps.get_app_config('core').get_models()

for model in app_models:
    admin.site.register(model)
