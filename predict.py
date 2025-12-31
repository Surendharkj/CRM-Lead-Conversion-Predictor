import pickle
import pandas as pd

# Load model
with open("model/lead_model.pkl", "rb") as f:
    model = pickle.load(f)

# New lead data
new_lead = pd.DataFrame([{
    "lead_source": 2,   # Website=2, Referral=1, Email=0 (depends on encoding)
    "calls_made": 4,
    "emails_sent": 2,
    "time_on_site": 10
}])

# Predict
prediction = model.predict(new_lead)

if prediction[0] == 1:
    print("🔥 Lead likely to convert")
else:
    print("❌ Lead unlikely to convert")
