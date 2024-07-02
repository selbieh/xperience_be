from django.contrib import admin
from .models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        all_fields = [field.name for field in obj._meta.get_fields()]
        return all_fields


admin.site.register(Transaction, TransactionAdmin)
