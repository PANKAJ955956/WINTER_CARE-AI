from pydantic import BaseModel, Field
from typing import List

class ScreeningCreate(BaseModel):
    age: int = Field(ge=0, le=120)
    temperature_c: float = Field(default=36.8, ge=30, le=45)
    symptoms: List[str] = Field(default_factory=list)
    risk_conditions: List[str] = Field(default_factory=list)
    breathing_difficulty: bool = False
    chest_pain: bool = False
    confusion: bool = False
    duration_days: int = Field(default=1, ge=0, le=365)

class EventCreate(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    location: str
    event_date: str
    expected_attendance: int = Field(ge=1, le=10000000)
    cold_exposure: str = "moderate"
    first_aid_posts: int = Field(default=1, ge=0)
    staff_count: int = Field(default=2, ge=0)
    checklist: List[str] = Field(default_factory=list)

class IncidentCreate(BaseModel):
    event_name: str
    incident_type: str
    severity: str = "moderate"
    description: str = ""
    action_taken: str = ""

class InventoryCreate(BaseModel):
    item_name: str
    category: str = "First aid"
    quantity: int = Field(ge=0)
    minimum_quantity: int = Field(default=5, ge=0)
    unit: str = "units"
