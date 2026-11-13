import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
BASE_DIR=Path(__file__).resolve().parent.parent
SECRET_KEY=os.getenv("DJANGO_SECRET_KEY","dev-only-change-before-deployment")
DEBUG=os.getenv("DEBUG","true").lower()=="true"
ALLOWED_HOSTS=["127.0.0.1","localhost"]
INSTALLED_APPS=["django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles","django_portal.ops"]
MIDDLEWARE=["django.middleware.security.SecurityMiddleware","django.contrib.sessions.middleware.SessionMiddleware","django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware"]
ROOT_URLCONF="django_portal.urls"
TEMPLATES=[{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.debug","django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION="django_portal.wsgi.application"
db_url=os.getenv("DATABASE_URL","sqlite:///./wintercare.db")
if db_url.startswith("sqlite:///"):
    db_name=str((BASE_DIR/db_url.replace("sqlite:///","")).resolve())
    DATABASES={"default":{"ENGINE":"django.db.backends.sqlite3","NAME":db_name}}
elif db_url.startswith("postgresql+psycopg://"):
    creds,hostdb=db_url.replace("postgresql+psycopg://","").split("@",1)
    user,password=creds.split(":",1); hostport,dbname=hostdb.split("/",1)
    host,port=(hostport.split(":")+["5432"])[:2]
    DATABASES={"default":{"ENGINE":"django.db.backends.postgresql","NAME":dbname,"USER":user,"PASSWORD":password,"HOST":host,"PORT":port}}
else: raise RuntimeError("Use sqlite:/// or postgresql+psycopg:// in DATABASE_URL")
LANGUAGE_CODE="en-us"; TIME_ZONE="Asia/Kolkata"; USE_I18N=True; USE_TZ=True
STATIC_URL="static/"; DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
