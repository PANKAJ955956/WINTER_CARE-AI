from django.db import models
class EventRegister(models.Model):
    name=models.CharField(max_length=160); location=models.CharField(max_length=200)
    event_date=models.DateField(); expected_attendance=models.PositiveIntegerField(default=100); notes=models.TextField(blank=True)
    def __str__(self): return self.name
class SupplyRegister(models.Model):
    item_name=models.CharField(max_length=120,unique=True); category=models.CharField(max_length=80,default="First aid")
    quantity=models.PositiveIntegerField(default=0); minimum_quantity=models.PositiveIntegerField(default=5)
    def __str__(self): return self.item_name
class IncidentRegister(models.Model):
    event_name=models.CharField(max_length=160); incident_type=models.CharField(max_length=100)
    severity=models.CharField(max_length=30,default="moderate"); description=models.TextField(blank=True)
    action_taken=models.TextField(blank=True); created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.event_name} — {self.incident_type}"
