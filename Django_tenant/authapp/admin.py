from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from authapp.models import Company, Domain

@admin.register(Company)
class CompanyAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ['schema_name', 'name', 'on_trial', 'trial_end', 'subcreption_id', 'subcreption_end', 'paid_date']
    
admin.site.register(Domain)