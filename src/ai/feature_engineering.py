import pandas as pd

from src.database.fetch_logs import fetch_logs


def build_dataset():

    logs = fetch_logs()

    df = pd.DataFrame(logs)

    # Convert timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Extract hour
    df["hour"] = df["timestamp"].dt.hour

    # Encode source
    source_map = {
        "Windows": 0,
        "Linux": 1,
        "Firewall": 2
    }

    df["source"] = df["source"].map(source_map)

    # Encode status
    status_map = {
        "Successful Login": 0,
        "Failed Login": 1,
        "ALLOW": 2,
        "DENY": 3,
        "File Open": 4
    }

    df["status"] = df["status"].map(status_map)

    # Encode severity
    severity_map = {
        "Low": 0,
        "Medium": 1,
        "High": 2
    }

    df["severity"] = df["severity"].map(severity_map)

    # Fill missing ports
    df["destination_port"] = df["destination_port"].fillna(0)

    features = df[
        [
            "hour",
            "source",
            "status",
            "severity",
            "destination_port"
        ]
    ]

    return features


if __name__ == "__main__":

    dataset = build_dataset()

    print(dataset.head())

    print("\nShape:", dataset.shape)