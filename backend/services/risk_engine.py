# Explainable educational score. This is not a diagnosis or clinically validated model.
def assess(payload):
    score, factors = 0, []
    if payload.breathing_difficulty:
        score += 60; factors.append("Breathing difficulty reported — urgent clinical assessment is important")
    if payload.chest_pain:
        score += 60; factors.append("Chest pain reported — urgent clinical assessment is important")
    if payload.confusion:
        score += 60; factors.append("Confusion reported — urgent clinical assessment is important")
    if payload.temperature_c >= 39:
        score += 20; factors.append("High reported temperature")
    elif payload.temperature_c >= 38:
        score += 12; factors.append("Elevated reported temperature")
    if payload.age < 5 or payload.age >= 65:
        score += 10; factors.append("Age group may need additional care")
    if payload.duration_days >= 5:
        score += 8; factors.append("Symptoms reported for five or more days")
    if payload.duration_days >= 10:
        score += 8; factors.append("Persistent symptoms reported")
    if payload.risk_conditions:
        score += min(20, 5 * len(payload.risk_conditions))
        factors.append("One or more pre-existing risk conditions selected")
    weights = {"shortness_of_breath":15,"wheezing":10,"fever":8,"persistent_cough":6,"dehydration":8}
    for symptom in payload.symptoms:
        if symptom in weights:
            score += weights[symptom]
            factors.append("Reported symptom: " + symptom.replace("_"," "))
    score = min(score, 100)
    emergency = payload.breathing_difficulty or payload.chest_pain or payload.confusion
    if emergency or score >= 60:
        level = "urgent"
        message = "Seek urgent medical assessment now. If this may be an emergency, contact local emergency services (India: 112). Do not rely on this app or delay care."
    elif score >= 30:
        level = "elevated"
        message = "Arrange timely advice from a qualified healthcare professional, especially if symptoms worsen. This tool cannot diagnose."
    else:
        level = "routine"
        message = "Use general self-care guidance and monitor symptoms. Contact a healthcare professional if symptoms persist, worsen, or concern you."
    return {"risk_score":score,"risk_level":level,"factors":factors or ["No additional risk factors selected"],"recommendation":message}
