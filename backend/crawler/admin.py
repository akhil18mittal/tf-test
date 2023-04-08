from django.contrib import admin

from .models import Loan


# Register your models here.


class CustomModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields if field.name not in ("id", "modified")]
        super(CustomModelAdmin, self).__init__(model, admin_site)


admin.site.register(Loan, CustomModelAdmin)