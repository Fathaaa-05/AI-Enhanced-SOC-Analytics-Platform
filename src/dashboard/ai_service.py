import joblib
import pandas as pd

from src.ai.feature_engineering import build_dataset
from src.database.fetch_logs import fetch_logs


def get_ai_anomalies():

    model = joblib.load("src/ai/model.pkl")

    dataset = build_dataset()

    predictions = model.predict(dataset)

    logs = fetch_logs()

    anomalies = []

    for i, prediction in enumerate(predictions):

        if prediction == -1:

            log = logs[i]

            anomalies.append({
                "timestamp": log["timestamp"],
                "username": log["username"],
                "source_ip": log["source_ip"],
                "source": log["source"],
                "status": log["status"],
                "severity": log["severity"]
            })

    return anomalies[:20]