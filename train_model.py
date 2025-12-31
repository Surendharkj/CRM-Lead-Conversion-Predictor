import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import pickle
import os

# Load data
data = pd.read_csv("data/leads.csv")

# Encode categorical column
le = LabelEncoder()
data["lead_source"] = le.fit_transform(data["lead_source"])

# Features & target
X = data.drop("converted", axis=1)
y = data["converted"]

# Train model
model = LogisticRegression()
model.fit(X, y)

# Save model + encoder
os.makedirs("model", exist_ok=True)
with open("model/lead_model.pkl", "wb") as f:
    pickle.dump((model, le), f)

print("✅ Model and encoder saved")
