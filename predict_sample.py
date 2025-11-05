# ===========================================================
# predict_sample.py — Jenkins Auto Prediction Script
# ===========================================================

import joblib
import numpy as np
import pandas as pd
import os

MODEL_PATH = "model.pkl"

print("\n🔍 Checking model file...")
if not os.path.exists(MODEL_PATH):
    print("❌ model.pkl not found. Please train the model first.")
    exit(1)

# Load trained model
model = joblib.load(MODEL_PATH)
print("✅ Model loaded successfully!\n")

# Define multiple test cases
# Columns assumed: [overs, wickets, runs_so_far, venue_factor]
test_cases = pd.DataFrame([
    [5.0, 1, 42, 1.0],
    [10.0, 2, 85, 1.05],
    [15.0, 3, 120, 0.95],
    [18.0, 4, 150, 1.1],
    [19.0, 6, 170, 0.9]
], columns=["overs", "wickets", "runs_so_far", "venue_factor"])

# Predict for all rows
predictions = model.predict(test_cases.values)

# Combine results into a table
test_cases["Predicted_Score"] = predictions.round(2)

print("🏏 IPL Score Predictions (from Jenkins):")
print(test_cases.to_string(index=False))

# Optionally save to CSV for artifact tracking
test_cases.to_csv("predicted_scores.csv", index=False)
print("\n✅ Predictions saved to predicted_scores.csv")
