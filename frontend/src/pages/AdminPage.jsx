import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../assets/style_A.css';

const AdminPage = () => {
  const [fakeNews, setFakeNews] = useState([]);
  const [message, setMessage] = useState('');
  const [newUser, setNewUser] = useState({
    user_id: '',
    password: '',
    role: 'J', // Default role is Journalist
  });
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    // Function to fetch fake news
    const fetchFakeNews = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/admin/overview', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        setFakeNews(response.data);
      } catch (error) {
        console.error('Error fetching fake news:', error);
      }
    };

    fetchFakeNews();
  }, []);

  // Function to show a message for 3 seconds
  const showMessage = (msg) => {
    setMessage(msg);
    setTimeout(() => {
      setMessage('');
    }, 3000);
  };

  // Function to navigate to the next fake news
  const goToNext = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % fakeNews.length);
  };

  // Function to navigate to the previous fake news
  const goToPrevious = () => {
    setCurrentIndex(
      (prevIndex) => (prevIndex - 1 + fakeNews.length) % fakeNews.length
    );
  };

  // Function to clear all users
  const clearUsers = async () => {
    try {
      const response = await axios.delete('http://127.0.0.1:8000/admin/clear-users', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      showMessage(`Success: ${response.data.message}`);
    } catch (error) {
      console.error('Error clearing users:', error);
    }
  };

  // Function to clear all fake news
  const clearFakeNews = async () => {
    try {
      const response = await axios.delete('http://127.0.0.1:8000/admin/clear-fake-news', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      showMessage(`Success: ${response.data.message}`);
      setFakeNews([]);
    } catch (error) {
      console.error('Error clearing fake news:', error);
    }
  };

  // Function to handle the logout
  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/";
  };

  // Function to register a new user
  const registerUser = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/users/register', newUser, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      showMessage(`Success: ${response.data.message}`);
      setNewUser({ user_id: '', password: '', role: 'J' });
    } catch (error) {
      console.error('Error registering user:', error);
    }
  };

  return (
    <div className="admin-container">
      <h2 className="admin-header">Admin Dashboard</h2>

      <div className="fake-news-section">
        <h3 className="section-title">Fake News Overview</h3>
        {fakeNews.length > 0 && (
          <div className="fake-news-window">
            <div className="fake-news-details">
              <h4>{fakeNews[currentIndex].description}</h4>
              <p>Generated Text: {fakeNews[currentIndex].generated_text}</p>
              <p>Fake Probability: {fakeNews[currentIndex].fake_probability}</p>
              <p>Image Path: {fakeNews[currentIndex].image_path}</p>
            </div>
            <div className="navigation-buttons">
              <button onClick={goToPrevious} className="nav-button">← Previous</button>
              <button onClick={goToNext} className="nav-button">Next →</button>
            </div>
          </div>
        )}
      </div>

      <div className="actions-section">
        <h3 className="section-title">Actions</h3>
        <button className="admin-button" onClick={clearUsers}>Clear All Users</button>
        <button className="admin-button" onClick={clearFakeNews}>Clear All Fake News</button>
      </div>

      <div className="register-section">
        <h3 className="section-title">Register New User</h3>
        <input
          className="input-field"
          type="text"
          placeholder="User ID"
          value={newUser.user_id}
          onChange={(e) => setNewUser({ ...newUser, user_id: e.target.value })}
        />
        <input
          className="input-field"
          type="password"
          placeholder="Password"
          value={newUser.password}
          onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
        />
        <select
          className="input-field"
          value={newUser.role}
          onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
        >
          <option value="J">Journalist</option>
          <option value="R">Researcher</option>
        </select>
        <button className="admin-button" onClick={registerUser}>Register</button>
      </div>

      <div className="logout-section">
        <button className="logout-button" onClick={handleLogout}>Logout</button>
      </div>

      {message && <p className="message">{message}</p>}
    </div>
  );
};

export default AdminPage;
