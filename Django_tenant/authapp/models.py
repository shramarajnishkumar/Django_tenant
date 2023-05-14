from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Company(TenantMixin):
    name = models.CharField(max_length=100)
    on_trial = models.BooleanField(default=True)
    trial_end = models.DateTimeField(null=True)
    subcreption_id = models.CharField(max_length=100, null=True) 
    subcreption_end = models.DateTimeField(null=True)
    paid_date = models.DateTimeField(null=True)
    auto_create_schema = True

class Domain(DomainMixin):
    pass