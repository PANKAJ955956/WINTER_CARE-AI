from django.contrib import admin
from .models import EventRegister,SupplyRegister,IncidentRegister
@admin.register(EventRegister)
class EventAdmin(admin.ModelAdmin):
    list_display=("name","location","event_date","expected_attendance"); search_fields=("name","location")
@admin.register(SupplyRegister)
class SupplyAdmin(admin.ModelAdmin):
    list_display=("item_name","category","quantity","minimum_quantity"); search_fields=("item_name",)
@admin.register(IncidentRegister)
class IncidentAdmin(admin.ModelAdmin):
    list_display=("event_name","incident_type","severity","created_at"); list_filter=("severity","incident_type")
