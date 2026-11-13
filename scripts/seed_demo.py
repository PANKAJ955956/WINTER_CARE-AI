import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from backend.database import Base,engine,SessionLocal
from backend import models
Base.metadata.create_all(bind=engine)
db=SessionLocal()
if db.query(models.InventoryItem).count()==0:
    db.add_all([
      models.InventoryItem(item_name="Disposable gloves",category="PPE",quantity=8,minimum_quantity=20,unit="boxes"),
      models.InventoryItem(item_name="First-aid kits",category="First aid",quantity=12,minimum_quantity=5,unit="kits"),
      models.InventoryItem(item_name="Drinking water",category="Hydration",quantity=180,minimum_quantity=100,unit="bottles"),
      models.InventoryItem(item_name="Thermal blankets",category="Equipment",quantity=14,minimum_quantity=25,unit="pieces")])
if db.query(models.HealthEvent).count()==0:
    db.add(models.HealthEvent(name="Winter Community Health Mela",location="Community Ground",event_date="2026-11-15",
      expected_attendance=1200,cold_exposure="moderate",first_aid_posts=2,staff_count=6,readiness_score=75,
      checklist="First-aid posts mapped; Drinking water available; Warm rest area; Trained staff briefing"))
if db.query(models.Incident).count()==0:
    db.add(models.Incident(event_name="Winter Community Health Mela",incident_type="Cold exposure",severity="low",
      description="Demo record: attendee requested a warm rest area.",action_taken="Directed to event rest area."))
db.commit(); db.close()
print("Demo records inserted where tables were empty.")
