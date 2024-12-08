import React, { useState } from 'react';
import { Button, TextField, Container, Typography, Box, Paper } from '@mui/material';
import axios from 'axios';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    humidity: '',
    pressure: '',
    wind_speed: '',
  });
  const [prediction, setPrediction] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loginData, setLoginData] = useState({ email: '', password: '' });
  const [registerData, setRegisterData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');

  const handlePredict = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/predict', formData, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPrediction(response.data.predicted_temperature);
      setError('');
    } catch (err) {
      setError('Error making prediction. Please try again.');
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      formData.append('username', loginData.email);
      formData.append('password', loginData.password);
      
      const response = await axios.post('http://localhost:8000/token', formData);
      setToken(response.data.access_token);
      localStorage.setItem('token', response.data.access_token);
      setError('');
    } catch (err) {
      setError('Login failed. Please check your credentials.');
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/register', registerData);
      setError('Registration successful! Please login.');
    } catch (err) {
      setError('Registration failed. Please try again.');
    }
  };

  return (
    <Container>
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Weather Temperature Prediction
        </Typography>
        
        {!token ? (
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
            <Paper sx={{ p: 3, width: 300 }}>
              <Typography variant="h5" gutterBottom>Login</Typography>
              <form onSubmit={handleLogin}>
                <TextField
                  fullWidth
                  margin="normal"
                  type="email"
                  label="Email"
                  value={loginData.email}
                  onChange={(e) => setLoginData({...loginData, email: e.target.value})}
                />
                <TextField
                  fullWidth
                  margin="normal"
                  type="password"
                  label="Password"
                  value={loginData.password}
                  onChange={(e) => setLoginData({...loginData, password: e.target.value})}
                />
                <Button 
                  fullWidth 
                  variant="contained" 
                  type="submit"
                  sx={{ mt: 2 }}
                >
                  Login
                </Button>
              </form>
            </Paper>

            <Paper sx={{ p: 3, width: 300 }}>
              <Typography variant="h5" gutterBottom>Register</Typography>
              <form onSubmit={handleRegister}>
                <TextField
                  fullWidth
                  margin="normal"
                  type="email"
                  label="Email"
                  value={registerData.email}
                  onChange={(e) => setRegisterData({...registerData, email: e.target.value})}
                />
                <TextField
                  fullWidth
                  margin="normal"
                  type="password"
                  label="Password"
                  value={registerData.password}
                  onChange={(e) => setRegisterData({...registerData, password: e.target.value})}
                />
                <Button 
                  fullWidth 
                  variant="contained" 
                  type="submit"
                  sx={{ mt: 2 }}
                >
                  Register
                </Button>
              </form>
            </Paper>
          </Box>
        ) : (
          <Paper sx={{ p: 3, maxWidth: 400, mx: 'auto' }}>
            <Button 
              variant="contained" 
              color="error"
              onClick={() => {
                setToken(null);
                localStorage.removeItem('token');
              }}
              sx={{ mb: 2 }}
            >
              Logout
            </Button>
            
            <form onSubmit={handlePredict}>
              <TextField
                fullWidth
                margin="normal"
                type="number"
                label="Humidity (%)"
                value={formData.humidity}
                onChange={(e) => setFormData({...formData, humidity: e.target.value})}
              />
              <TextField
                fullWidth
                margin="normal"
                type="number"
                label="Pressure (hPa)"
                value={formData.pressure}
                onChange={(e) => setFormData({...formData, pressure: e.target.value})}
              />
              <TextField
                fullWidth
                margin="normal"
                type="number"
                label="Wind Speed (km/h)"
                value={formData.wind_speed}
                onChange={(e) => setFormData({...formData, wind_speed: e.target.value})}
              />
              <Button 
                fullWidth 
                variant="contained" 
                type="submit"
                sx={{ mt: 2 }}
              >
                Predict Temperature
              </Button>
            </form>

            {prediction !== null && (
              <Box sx={{ mt: 2, p: 2, bgcolor: 'primary.light', borderRadius: 1 }}>
                <Typography variant="h6">
                  Predicted Temperature: {prediction.toFixed(2)}°C
                </Typography>
              </Box>
            )}
          </Paper>
        )}

        {error && (
          <Typography color="error" sx={{ mt: 2 }}>
            {error}
          </Typography>
        )}
      </Box>
    </Container>
  );
}

export default App;