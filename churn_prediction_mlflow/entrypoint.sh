#!/bin/bash
set -e

echo "Starting MLflow tracking server..."

# Start MLflow server in background using the correct conda env
conda run -n churn_prediction --no-capture-output mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns \
  --host 0.0.0.0 --port 5000 &

# Wait briefly for MLflow server to start
sleep 5

# Loop over hyperparameters and train models using conda
for test_size in 0.2 0.4; do
  for n_estimators in 100 150 200; do
    echo "Training: test_size=${test_size}, n_estimators=${n_estimators}"
    conda run -n churn_prediction --no-capture-output python train.py \
      --data_path data.csv \
      --test_size $test_size \
      --n_estimators $n_estimators
  done
done

echo "Training End..."

# Keep container alive
tail -f /dev/null

