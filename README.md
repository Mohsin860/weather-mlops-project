# Weather Prediction MLOps Project

## Project Overview
A comprehensive MLOps pipeline implementing weather temperature prediction with modern DevOps and MLOps practices. The project includes data versioning, model tracking, automated workflows, and full-stack deployment capabilities.

## Features
- Data version control using DVC
- Model tracking and versioning with MLFlow
- Automated workflows using Apache Airflow
- FastAPI backend with prediction endpoints
- React frontend for user interaction
- User authentication and database integration
- CI/CD pipeline with Docker and Kubernetes
- Branch-based workflow with automated testing

## Architecture
![Project Architecture]
- Frontend: React application with Material-UI
- Backend: FastAPI with scikit-learn model serving
- Database: SQLite for user authentication
- MLOps Tools: DVC, MLFlow, Airflow
- Deployment: Docker containers, Kubernetes orchestration

## Prerequisites
- Python 3.9+
- Node.js and npm
- Docker Desktop
- Minikube
- Git

## Installation

1. Clone the repository
```bash
git clone <repository-url>
cd weather-mlops-project
```

2. Set up Python environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. Start MLflow server
```bash
mlflow server --host 0.0.0.0 --port 5000
```

4. Start Airflow (using Docker)
```bash
docker-compose -f docker-compose-airflow.yml up -d
```

5. Set up and start backend
```bash
cd backend
uvicorn api.main:app --reload
```

6. Set up and start frontend
```bash
cd frontend
npm install
npm start
```

## Project Components

### 1. Data Pipeline
- Location: `data/`
- Versioned using DVC
- Automated updates via Airflow DAGs
- Commands:
```bash
dvc init
dvc add data/weather_data.csv
dvc push
```

### 2. Model Training
- Location: `models/`
- RandomForest model for temperature prediction
- Tracked using MLFlow
- Commands:
```bash
python models/train.py
```

### 3. Backend API
- Location: `backend/`
- FastAPI implementation
- Endpoints:
  - POST /predict: Weather prediction
  - POST /register: User registration
  - POST /token: User authentication
- Start server:
```bash
uvicorn backend.api.main:app --reload
```

### 4. Frontend Application
- Location: `frontend/`
- React with Material-UI
- Features:
  - User registration/login
  - Weather prediction interface
  - Real-time results display
- Start application:
```bash
npm start
```

### 5. MLOps Configuration
- MLFlow tracking
- DVC data versioning
- Airflow DAGs for automation
- Access UIs:
  - MLFlow: http://localhost:5000
  - Airflow: http://localhost:8080
  - API Docs: http://localhost:8000/docs

## Branch Structure
- `dev`: Development branch
- `testing`: Automated testing workflows
- `prod`: Production deployment
- Workflow:
  1. Develop in `dev`
  2. Merge to `testing` for automated tests
  3. Deploy to `prod` after successful tests

## Usage Instructions

1. Start all services:
```bash
# Terminal 1: MLflow
mlflow server --host 0.0.0.0 --port 5000

# Terminal 2: Backend
cd backend
uvicorn api.main:app --reload

# Terminal 3: Frontend
cd frontend
npm start
```

2. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs
- MLflow UI: http://localhost:5000
- Airflow UI: http://localhost:8080

3. User Workflow:
   - Register a new account
   - Login with credentials
   - Input weather parameters:
     - Humidity (30-100%)
     - Pressure (980-1020 hPa)
     - Wind Speed (0-30 km/h)
   - View temperature predictions

## Project Structure
```
weather-mlops-project/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── airflow/
│   └── dags/
│       └── training_pipeline.py
├── backend/
│   ├── api/
│   │   ├── main.py
│   │   └── models.py
│   ├── tests/
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   └── components/
│   └── Dockerfile
├── data/
│   └── weather_data.csv
├── models/
│   └── train.py
├── kubernetes/
│   ├── frontend-deployment.yaml
│   ├── backend-deployment.yaml
│   └── database-deployment.yaml
├── docker-compose.yml
├── docker-compose-airflow.yml
├── requirements.txt
└── README.md
```

## Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Deployment

1. Build Docker images:
```bash
docker-compose build
```

2. Deploy to Kubernetes:
```bash
kubectl apply -f kubernetes/
```

## Monitoring

- Model performance metrics: Available in MLFlow UI
- Application logs: Docker logs
- Pipeline status: Airflow UI
- API documentation: Swagger UI at /docs endpoint

## Troubleshooting

1. MLFlow connection issues:
   - Verify MLFlow server is running
   - Check port 5000 availability

2. Database connection:
   - Verify SQLite file permissions
   - Check connection string

3. Docker issues:
   - Ensure Docker Desktop is running
   - Check container logs

## Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## License
This project is licensed under the MIT License.

## Acknowledgments
- MLOps community
- FastAPI documentation
- React documentation
- MLFlow documentation