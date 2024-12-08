from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import mlflow
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import os

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 12, 8),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def generate_data():
    """Generate sample weather data"""
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'humidity': np.random.uniform(30, 100, n_samples),
        'pressure': np.random.uniform(980, 1020, n_samples),
        'wind_speed': np.random.uniform(0, 30, n_samples),
    }
    
    data['temperature'] = (
        25 +
        -0.1 * (data['humidity'] - 65) +
        0.1 * (data['pressure'] - 1000) +
        -0.2 * data['wind_speed'] +
        np.random.normal(0, 2, n_samples)
    )
    
    df = pd.DataFrame(data)
    df.to_csv('data/weather_data.csv', index=False)
    return "Data generated successfully"

def train_model():
    """Train the weather prediction model"""
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("weather_prediction")
    
    # Read data
    df = pd.read_csv('data/weather_data.csv')
    
    X = df[['humidity', 'pressure', 'wind_speed']]
    y = df['temperature']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    with mlflow.start_run() as run:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Log metrics
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        
        mlflow.log_metric("train_r2", train_score)
        mlflow.log_metric("test_r2", test_score)
        
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        # Save run ID
        with open('models/latest_model.txt', 'w') as f:
            f.write(run.info.run_id)
    
    return "Model trained successfully"

def evaluate_model():
    """Evaluate model performance"""
    with open('models/latest_model.txt', 'r') as f:
        run_id = f.read().strip()
    
    mlflow.set_tracking_uri("http://localhost:5000")
    client = mlflow.tracking.MlflowClient()
    run = client.get_run(run_id)
    metrics = run.data.metrics
    
    # Log evaluation results
    with open('model_evaluation.txt', 'w') as f:
        f.write(f"Model Performance Metrics:\n")
        f.write(f"Train R2: {metrics['train_r2']:.4f}\n")
        f.write(f"Test R2: {metrics['test_r2']:.4f}\n")
    
    return "Model evaluated successfully"

# Create DAG
dag = DAG(
    'weather_prediction_pipeline',
    default_args=default_args,
    description='A DAG for weather prediction model training pipeline',
    schedule_interval=timedelta(days=1),
    catchup=False
)

# Define tasks
generate_data_task = PythonOperator(
    task_id='generate_data',
    python_callable=generate_data,
    dag=dag,
)

train_model_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag,
)

evaluate_model_task = PythonOperator(
    task_id='evaluate_model',
    python_callable=evaluate_model,
    dag=dag,
)

# Set task dependencies
generate_data_task >> train_model_task >> evaluate_model_task