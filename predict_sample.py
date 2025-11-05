# ===========================================================
# predict_sample.py - Jenkins Safe ASCII Version
# ===========================================================

import joblib
import numpy as np
import os
import pandas as pd

MODEL_PATH = "model.pkl"

print("\n--- Checking model file ---")
if not os.path.exists(MODEL_PATH):
    print("ERROR: Model not found. Please train the model first.")
    exit(1)

# Load the trained model
print("Model found. Loading model...")
model = joblib.load(MODEL_PATH)
print("Model loaded successfully.\n")

# Sample test inputs
# Columns order: [overs, wickets, runs_so_far, venue_factor]
test_cases = [
    [5.0, 1, 42, 1.00],
    [10.0, 2, 85, 1.05],
    [15.0, 3, 120, 0.95],
    [18.0, 4, 150, 1.10],
    [19.0, 6, 170, 0.90],
]

print("Running sample IPL score predictions...")
inputs = np.array(test_cases)

# Predict using the trained model
preds = model.predict(inputs)

# Combine input and output into table
results = pd.DataFrame(test_cases, columns=["overs", "wickets", "runs_so_far", "venue_factor"])
results["Predicted_Score"] = preds.round(2)

print("\n--- IPL Score Predictions (Jenkins Output) ---")
print(results.to_string(index=False))

# Save to CSV for artifact collection
results.to_csv("predicted_scores.csv", index=False)
print("\nPredictions saved to predicted_scores.csv\n")
