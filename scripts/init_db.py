import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from backend.database import Base,engine
from backend import models
Base.metadata.create_all(bind=engine)
print("WinterCare application database tables are ready.")
