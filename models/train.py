import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import mlflow
import mlflow.sklearn
from datetime import datetime

# Configure MLFlow
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("weather_prediction")

# Generate sample weather data
def generate_sample_data(n_samples=1000):
    np.random.seed(42)
    data = {
        'humidity': np.random.uniform(30, 100, n_samples),
        'pressure': np.random.uniform(980, 1020, n_samples),
        'wind_speed': np.random.uniform(0, 30, n_samples),
        'temperature': []
    }
    
    # Generate temperature with some correlation to other features
    for i in range(n_samples):
        temp = (
            25 +  # base temperature
            -0.1 * (data['humidity'][i] - 65) +  # humidity effect
            0.1 * (data['pressure'][i] - 1000) +  # pressure effect
            -0.2 * data['wind_speed'][i] +  # wind effect
            np.random.normal(0, 2)  # random variation
        )
        data['temperature'].append(temp)
    
    return pd.DataFrame(data)

def train_model():
    # Generate and save sample data
    data = generate_sample_data()
    data.to_csv('data/weather_data.csv', index=False)
    
    # Prepare features and target
    X = data[['humidity', 'pressure', 'wind_speed']]
    y = data['temperature']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    with mlflow.start_run():
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Calculate metrics
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        
        # Log parameters and metrics
        mlflow.log_param("n_estimators", 100)
        mlflow.log_metric("train_r2", train_score)
        mlflow.log_metric("test_r2", test_score)
        
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        print(f"Training Score: {train_score}")
        print(f"Test Score: {test_score}")
        
        # Save model ID
        run_id = mlflow.active_run().info.run_id
        with open('models/latest_model.txt', 'w') as f:
            f.write(run_id)

if __name__ == "__main__":
    train_model()