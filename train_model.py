import mlflow
import os
import mlflow.sklearn
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

def train_and_save_model():
    # Set MLflow tracking URI
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("weather_prediction")

    # Generate sample data
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'humidity': np.random.uniform(30, 100, n_samples),
        'pressure': np.random.uniform(980, 1020, n_samples),
        'wind_speed': np.random.uniform(0, 30, n_samples),
    }
    
    # Generate temperature with correlations
    data['temperature'] = (
        25 +  # base temperature
        -0.1 * (data['humidity'] - 65) +  # humidity effect
        0.1 * (data['pressure'] - 1000) +  # pressure effect
        -0.2 * data['wind_speed'] +  # wind effect
        np.random.normal(0, 2, n_samples)  # random variation
    )
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Split features and target
    X = df[['humidity', 'pressure', 'wind_speed']]
    y = df['temperature']
    
    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
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
        
        print(f"Model trained and saved with run_id: {run.info.run_id}")
        print(f"Train R2: {train_score}")
        print(f"Test R2: {test_score}")

if __name__ == "__main__":
    train_and_save_model()