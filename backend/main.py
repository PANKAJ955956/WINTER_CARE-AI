from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from datetime import datetime
from .database import Base, engine, get_db
from . import models, schemas
from .services.risk_engine import assess
from .services.wellness import get_guide

Base.metadata.create_all(bind=engine)
app = FastAPI(title="WinterCare AI API", version="1.0.0", description="Winter wellness and festival health operations demo API. Not for diagnosis.")

@app.get("/health")
def health():
    return {"status":"ok","service":"WinterCare AI API","timestamp":datetime.utcnow().isoformat()}

@app.get("/api/v1/dashboard")
def dashboard(db:Session=Depends(get_db)):
    return {"total_screenings":db.query(models.Screening).count(),
      "urgent_screenings":db.query(models.Screening).filter(models.Screening.risk_level=="urgent").count(),
      "events":db.query(models.HealthEvent).count(),"incidents":db.query(models.Incident).count(),
      "low_stock_items":db.query(models.InventoryItem).filter(models.InventoryItem.quantity<models.InventoryItem.minimum_quantity).count()}

@app.post("/api/v1/screenings")
def create_screening(payload:schemas.ScreeningCreate, db:Session=Depends(get_db)):
    result=assess(payload)
    row=models.Screening(age=payload.age,temperature_c=payload.temperature_c,symptoms=",".join(payload.symptoms),
      risk_conditions=",".join(payload.risk_conditions),breathing_difficulty=payload.breathing_difficulty,
      chest_pain=payload.chest_pain,confusion=payload.confusion,duration_days=payload.duration_days,
      risk_score=result["risk_score"],risk_level=result["risk_level"],factors="; ".join(result["factors"]),
      recommendation=result["recommendation"])
    db.add(row); db.commit(); db.refresh(row)
    return {"id":row.id,**result,"created_at":row.created_at.isoformat()}

@app.get("/api/v1/screenings")
def list_screenings(limit:int=50,db:Session=Depends(get_db)):
    rows=db.query(models.Screening).order_by(desc(models.Screening.created_at)).limit(min(limit,200)).all()
    return [{"id":r.id,"age":r.age,"risk_score":r.risk_score,"risk_level":r.risk_level,"temperature_c":r.temperature_c,
      "factors":r.factors,"created_at":r.created_at.isoformat()} for r in rows]

@app.post("/api/v1/events")
def create_event(payload:schemas.EventCreate,db:Session=Depends(get_db)):
    score=0
    score += 25 if payload.first_aid_posts>=max(1,payload.expected_attendance//5000) else 10
    score += 25 if payload.staff_count>=max(2,payload.expected_attendance//1000) else 10
    score += 25 if len(payload.checklist)>=4 else 10
    score += 25 if payload.cold_exposure.lower() in ("low","moderate") else 10
    row=models.HealthEvent(name=payload.name,location=payload.location,event_date=payload.event_date,
      expected_attendance=payload.expected_attendance,cold_exposure=payload.cold_exposure,
      first_aid_posts=payload.first_aid_posts,staff_count=payload.staff_count,readiness_score=min(score,100),
      checklist="; ".join(payload.checklist))
    db.add(row); db.commit(); db.refresh(row)
    return {"id":row.id,"name":row.name,"readiness_score":row.readiness_score,
      "status":"Ready for review" if row.readiness_score>=75 else "Action required"}

@app.get("/api/v1/events")
def list_events(db:Session=Depends(get_db)):
    rows=db.query(models.HealthEvent).order_by(desc(models.HealthEvent.created_at)).all()
    return [{"id":r.id,"name":r.name,"location":r.location,"event_date":r.event_date,
      "expected_attendance":r.expected_attendance,"readiness_score":r.readiness_score,
      "staff_count":r.staff_count,"first_aid_posts":r.first_aid_posts} for r in rows]

@app.post("/api/v1/incidents")
def create_incident(payload:schemas.IncidentCreate,db:Session=Depends(get_db)):
    row=models.Incident(**payload.model_dump()); db.add(row); db.commit(); db.refresh(row)
    return {"id":row.id,"message":"Incident logged","severity":row.severity}

@app.get("/api/v1/incidents")
def list_incidents(db:Session=Depends(get_db)):
    rows=db.query(models.Incident).order_by(desc(models.Incident.created_at)).limit(100).all()
    return [{"id":r.id,"event_name":r.event_name,"incident_type":r.incident_type,"severity":r.severity,
      "description":r.description,"action_taken":r.action_taken,"created_at":r.created_at.isoformat()} for r in rows]

@app.post("/api/v1/inventory")
def upsert_inventory(payload:schemas.InventoryCreate,db:Session=Depends(get_db)):
    row=db.query(models.InventoryItem).filter(func.lower(models.InventoryItem.item_name)==payload.item_name.lower()).first()
    if row:
        for k,v in payload.model_dump().items(): setattr(row,k,v)
    else:
        row=models.InventoryItem(**payload.model_dump()); db.add(row)
    db.commit(); db.refresh(row)
    return {"id":row.id,"item_name":row.item_name,"quantity":row.quantity,"minimum_quantity":row.minimum_quantity}

@app.get("/api/v1/inventory")
def list_inventory(db:Session=Depends(get_db)):
    rows=db.query(models.InventoryItem).order_by(models.InventoryItem.item_name).all()
    return [{"id":r.id,"item_name":r.item_name,"category":r.category,"quantity":r.quantity,
      "minimum_quantity":r.minimum_quantity,"unit":r.unit,"low_stock":r.quantity<r.minimum_quantity} for r in rows]

@app.get("/api/v1/wellness/{category}")
def wellness(category:str):
    return get_guide(category)
