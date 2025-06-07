#!/bin/bash
set -e

echo "Starting MLflow tracking server..."
conda run -n churn_prediction mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns \
  -h 0.0.0.0 -p 5000 &  # Run in background

# Give it a few seconds to start
sleep 5

echo "Training model 1..."
conda run -n churn_prediction python train.py --data_path data.csv --test_size 0.2 --n_estimators 100

echo "Training model 2..."
conda run -n churn_prediction python train.py --data_path data.csv --test_size 0.4 --n_estimators 100

echo "Training model 3..."
conda run -n churn_prediction python train.py --data_path data.csv --test_size 0.2 --n_estimators 150

echo "Training model 4..."
conda run -n churn_prediction python train.py --data_path data.csv --test_size 0.4 --n_estimators 150

echo "Training model 5..."
conda run -n churn_prediction python train.py --data_path data.csv --test_size 0.4 --n_estimators 200

echo "Training model 6..."
conda run -n churn_prediction python train.py --data_path data.csv --test_size 0.2 --n_estimators 200


tail -f /dev/null
