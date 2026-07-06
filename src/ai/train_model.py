import joblib
from sklearn.ensemble import IsolationForest

from src.ai.feature_engineering import build_dataset


def train_model():

    print("Loading dataset...")

    dataset = build_dataset()

    print(f"Dataset shape: {dataset.shape}")

    model = IsolationForest(
        n_estimators=100,
        contamination=0.03,
        random_state=42
    )

    print("Training AI model...")

    model.fit(dataset)

    joblib.dump(model, "src/ai/model.pkl")

    print("\n✅ AI Model Trained Successfully!")
    print("📁 Model saved as src/ai/model.pkl")


if __name__ == "__main__":
    train_model()