import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import '../assets/style.css';

const Home = () => {
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [user, setUser] = useState(null); // State to manage the user
  const [loading, setLoading] = useState(false); // State to manage the loading indicator
  const navigate = useNavigate();

  // useEffect to retrieve the user from the token stored in local storage
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      const decoded = jwtDecode(token);
      setUser({ user_id: decoded.sub, role: decoded.role });
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); 

    try {
      const response = await axios.post('http://127.0.0.1:8000/users/login', {
        user_id: userId,
        password,
      });

      if (response.data.token) {
        const token = response.data.token;
        localStorage.setItem('token', token);

        // Decode the token to get the user information
        const decoded = jwtDecode(token);
        const loggedUser = { user_id: decoded.sub, role: decoded.role };

        // Set the user in the state
        setUser(loggedUser);

        // Navigate to the corresponding page based on the role
        const rolePaths = {
          'A': '/admin',
          'R': '/researcher',
          'J': '/journalist',
        };

        window.location.href = rolePaths[loggedUser.role];
      } else {
        setError('Invalid credentials');
      }
    } catch (error) {
      setError('Invalid credentials');
    } finally {
      setLoading(false); 
    }
  };

  return (
    <div>
      <h1>Want to be fake? Just enter your account!</h1>
      <div>
        <h2>Login</h2>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="User ID"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button type="submit" disabled={loading}>Login</button>
        </form>
        {loading && <p>Loading...</p>}
      </div>
    </div>
  );
};

export default Home;
