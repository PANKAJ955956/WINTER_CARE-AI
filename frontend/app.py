import os, requests
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
API=os.getenv("API_BASE_URL","http://127.0.0.1:8000")
st.set_page_config(page_title="WinterCare AI",page_icon="❄️",layout="wide")
st.markdown('''<style>
.main{background:linear-gradient(180deg,rgba(224,242,254,.18),transparent 260px)}
.hero{padding:1.3rem 1.5rem;border-radius:18px;background:linear-gradient(110deg,#0f3557,#176b87);color:white;margin-bottom:1rem}
.hero h1{color:white;margin:0}.hero p{color:#d9f4ff;margin:.35rem 0 0}
</style>''',unsafe_allow_html=True)
def api(method,path,**kwargs):
    try:
        r=requests.request(method,f"{API}{path}",timeout=5,**kwargs); r.raise_for_status(); return r.json(),None
    except requests.RequestException as e: return None,str(e)
with st.sidebar:
    st.title("❄️ WinterCare AI")
    page=st.radio("Workspace",["Overview","Health Screening","Winter Wellness","Festival Readiness","Inventory","Incident Desk","API Status"])
    st.caption("Winter health • Festival safety • AI-assisted operations")
    st.divider(); st.caption(f"API: {API}")
st.markdown('<div class="hero"><h1>WinterCare AI</h1><p>Winter wellness intelligence & festival health operations command centre</p></div>',unsafe_allow_html=True)
st.warning("Demo software only — not a diagnosis or medical advice. Use fictional data only. In an emergency, contact local emergency services (India: 112).")

if page=="Overview":
    data,err=api("GET","/api/v1/dashboard")
    if err: st.error(f"API unavailable: {err}. Start FastAPI using the README command.")
    else:
        cols=st.columns(5)
        for col,(label,key) in zip(cols,[("Screenings","total_screenings"),("Urgent flags","urgent_screenings"),("Events","events"),("Incidents","incidents"),("Low stock","low_stock_items")]):
            col.metric(label,data[key])
    st.subheader("Operational priorities")
    a,b,c=st.columns(3)
    a.info("🧣 Cold-weather readiness\n\nPromote layered clothing, safe heating and checks on vulnerable attendees.")
    b.info("🩺 Health screening\n\nUse screening only as a non-diagnostic prompt for follow-up.")
    c.info("🎪 Event preparedness\n\nConfirm first-aid coverage, water, sanitation, access and escalation plans.")
    events,_=api("GET","/api/v1/events")
    if events: st.subheader("Registered events"); st.dataframe(pd.DataFrame(events),use_container_width=True,hide_index=True)

elif page=="Health Screening":
    st.subheader("Winter symptom screening")
    st.caption("Fictional/demo information only. The score is not a diagnosis.")
    with st.form("screen"):
        c1,c2,c3=st.columns(3)
        age=c1.number_input("Age",0,120,30); temp=c2.number_input("Temperature (°C)",30.0,45.0,36.8,.1); duration=c3.number_input("Duration (days)",0,365,2)
        symptoms=st.multiselect("Reported symptoms",["cough","sore_throat","fever","persistent_cough","wheezing","shortness_of_breath","dehydration","body_ache","runny_nose"])
        conditions=st.multiselect("Relevant risk conditions",["asthma","diabetes","heart_condition","immune_suppression","chronic_lung_condition"])
        x,y,z=st.columns(3); breath=x.checkbox("Breathing difficulty"); chest=y.checkbox("Chest pain"); confusion=z.checkbox("Confusion")
        submitted=st.form_submit_button("Assess and save screening",type="primary")
    if submitted:
        payload={"age":int(age),"temperature_c":temp,"duration_days":int(duration),"symptoms":symptoms,"risk_conditions":conditions,
          "breathing_difficulty":breath,"chest_pain":chest,"confusion":confusion}
        result,err=api("POST","/api/v1/screenings",json=payload)
        if err: st.error(err)
        else:
            st.metric("Screening flag",result["risk_level"].upper(),f"Score {result['risk_score']}/100")
            if result["risk_level"]=="urgent": st.error(result["recommendation"])
            elif result["risk_level"]=="elevated": st.warning(result["recommendation"])
            else: st.success(result["recommendation"])
            st.write("**Factors considered**")
            for f in result["factors"]: st.write("•",f)
    rows,err=api("GET","/api/v1/screenings")
    if rows: st.subheader("Recent screenings"); st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

elif page=="Winter Wellness":
    st.subheader("Winter wellness knowledge centre")
    topics={"Cold & flu season":"cold_flu","Cold-weather safety":"cold_safety","Hydration & nutrition":"hydration_nutrition","Festival crowd health":"festival_crowd"}
    choice=st.selectbox("Choose a topic",list(topics))
    guide,err=api("GET",f"/api/v1/wellness/{topics[choice]}")
    if err: st.error(err)
    else:
        st.markdown(f"### {guide['title']}")
        for point in guide["points"]: st.markdown(f"- {point}")
        st.info(guide["seek"])

elif page=="Festival Readiness":
    st.subheader("Festival / public event health readiness")
    with st.form("event"):
        name=st.text_input("Event name","Winter Wellness & Community Festival")
        location=st.text_input("Location","Community Ground"); date=st.date_input("Event date")
        c1,c2,c3=st.columns(3)
        attendance=c1.number_input("Expected attendance",1,10000000,1200)
        posts=c2.number_input("First-aid posts",0,1000,2); staff=c3.number_input("Trained health staff",0,10000,6)
        cold=st.selectbox("Expected cold exposure",["low","moderate","high"])
        checklist=st.multiselect("Readiness checklist",["First-aid posts mapped","Emergency access route clear","Drinking water available","Handwashing and sanitation","Warm rest area","Emergency contacts displayed","Crowd communication plan","Trained staff briefing"])
        save=st.form_submit_button("Calculate readiness & register event",type="primary")
    if save:
        payload={"name":name,"location":location,"event_date":str(date),"expected_attendance":int(attendance),"first_aid_posts":int(posts),
          "staff_count":int(staff),"cold_exposure":cold,"checklist":checklist}
        result,err=api("POST","/api/v1/events",json=payload)
        if err: st.error(err)
        else:
            st.metric("Readiness heuristic",f"{result['readiness_score']}%")
            st.success(f"Event saved. {result['status']}")
            st.caption("Illustrative planning heuristic, not a regulatory standard.")
    events,err=api("GET","/api/v1/events")
    if events: st.subheader("Registered events"); st.dataframe(pd.DataFrame(events),use_container_width=True,hide_index=True)

elif page=="Inventory":
    st.subheader("Medical supply inventory")
    with st.form("stock"):
        c1,c2,c3=st.columns(3)
        item=c1.text_input("Supply item","Disposable gloves"); category=c2.selectbox("Category",["PPE","First aid","Hydration","Equipment","Sanitation"]); unit=c3.text_input("Unit","boxes")
        a,b=st.columns(2); qty=a.number_input("Current quantity",0,100000,20); minimum=b.number_input("Minimum quantity",0,100000,10)
        save=st.form_submit_button("Save inventory item")
    if save:
        res,err=api("POST","/api/v1/inventory",json={"item_name":item,"category":category,"quantity":int(qty),"minimum_quantity":int(minimum),"unit":unit})
        if err: st.error(err)
        else: st.success(f"Saved {res['item_name']}")
    rows,err=api("GET","/api/v1/inventory")
    if rows:
        df=pd.DataFrame(rows); st.dataframe(df,use_container_width=True,hide_index=True)
        low=df[df["low_stock"]]
        if len(low): st.warning("Replenishment needed: "+", ".join(low["item_name"].tolist()))
        else: st.success("No low-stock items flagged.")

elif page=="Incident Desk":
    st.subheader("Event incident log")
    with st.form("incident"):
        event=st.text_input("Event name"); kind=st.selectbox("Incident type",["Cold exposure","Fall / injury","Crowd distress","Dehydration","Respiratory concern","Other"])
        severity=st.selectbox("Severity",["low","moderate","high","critical"])
        description=st.text_area("Factual summary (no identifying details)"); action=st.text_area("Action taken / escalation")
        save=st.form_submit_button("Log incident",type="primary")
    if save:
        res,err=api("POST","/api/v1/incidents",json={"event_name":event,"incident_type":kind,"severity":severity,"description":description,"action_taken":action})
        if err: st.error(err)
        else: st.success("Incident logged.")
    rows,err=api("GET","/api/v1/incidents")
    if rows: st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)

elif page=="API Status":
    st.subheader("Backend connectivity")
    data,err=api("GET","/health")
    if err: st.error(f"FastAPI is not reachable: {err}")
    else: st.success(f"Connected — {data['service']} ({data['status']})")
    st.markdown(f"Swagger: [{API}/docs]({API}/docs)")
