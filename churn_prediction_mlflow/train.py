import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn
import matplotlib.pyplot as plt

mlflow.set_tracking_uri("http://127.0.0.1:5000")


def load_data(data_path):
    df = pd.read_csv(data_path)
    df = df.dropna()
    df = df.drop("customerID", axis=1)
    df["Churn"] = df["Churn"].map({"No": 0, "Yes": 1})
    df = pd.get_dummies(df)
    X = df.drop("Churn", axis=1)
    y = df["Churn"]
    return X, y

def train_model(X_train, y_train, n_estimators):
    model = RandomForestClassifier(n_estimators=n_estimators)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy

def log_feature_importance(model, feature_names):
    importance = model.feature_importances_
    importance_df = pd.DataFrame({"Feature": feature_names, "Importance": importance})
    importance_df = importance_df.sort_values(by="Importance", ascending=False)
    print("\nTop Important Features:\n", importance_df.head(10))
    plt.barh(feature_names, importance)
    plt.title("Feature Importance")
    plt.savefig("feature_importance.png")
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, default="data.csv")
    parser.add_argument("--test_size", type=float, default=0.2)
    parser.add_argument("--n_estimators", type=int, default=100)  # ✅ Add this line
    args = parser.parse_args()

    # Load data
    X, y = load_data(args.data_path)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=args.test_size)

    # MLflow tracking
    try:
        with mlflow.start_run():
            model = train_model(X_train, y_train, n_estimators=args.n_estimators)  # ✅ Pass param
            accuracy = evaluate_model(model, X_test, y_test)

            mlflow.log_param("n_estimators", args.n_estimators)  # ✅ Log param
            mlflow.log_param("test_size", args.test_size)
            mlflow.log_metric("accuracy", accuracy)

            mlflow.sklearn.log_model(model, "model")
            log_feature_importance(model, X.columns)
            mlflow.log_artifact("feature_importance.png")

    except Exception as e:
        print(f"MLflow tracking failed: {str(e)}")
