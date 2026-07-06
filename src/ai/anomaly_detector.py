import joblib

from src.ai.feature_engineering import build_dataset


def detect_anomalies():

    model = joblib.load("src/ai/model.pkl")

    dataset = build_dataset()

    predictions = model.predict(dataset)

    dataset["prediction"] = predictions

    anomalies = dataset[dataset["prediction"] == -1]

    print(f"\nTotal Records : {len(dataset)}")
    print(f"AI Anomalies  : {len(anomalies)}\n")

    print(anomalies.head(20))

    return anomalies


if __name__ == "__main__":
    detect_anomalies()