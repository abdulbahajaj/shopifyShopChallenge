from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Product)
admin.site.register(models.Cart)
admin.site.register(models.CartProductMap)