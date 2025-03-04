import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../assets/style_JR.css';

const JournalistPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [description, setDescription] = useState('');
  const [fakeNews, setFakeNews] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  // Function to manage the file selection
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  // Function to generate fake news
  const generateFakeNews = async () => {
    if (!selectedFile) {
      setMessage('Select a file.');
      return;
    }

    // Reset the state
    setDescription('');
    setFakeNews('');
    setMessage('Preparing response...');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/fake-news/generate-fake-news',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        }
      );

      setDescription(response.data.description);
      setFakeNews(response.data.fake_news);
      setMessage('');
    } catch (error) {
      setMessage('Error in generating fake news.');
      console.error(error);
    }
  };

  // Funzione per il logout
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    navigate('/');
  };

  return (
    <div className="journalist-page-container">
      <h2 className="page-title">Journalist Dashboard</h2>

      <button className="logout-button" onClick={handleLogout}>
        Logout
      </button>

      <div className="upload-section">
        <h3>Upload an Image to Generate Fake News</h3>
        <input type="file" onChange={handleFileChange} />
        <button className="generate-button" onClick={generateFakeNews}>Generate</button>
      </div>

      {message && <p className="message">{message}</p>}

      <div className="scrollable-container">
        {description && (
          <div className="output-box">
            <h3>Generated Description</h3>
            <p>{description}</p>
          </div>
        )}

        {fakeNews && (
          <div className="output-box">
            <h3>Generated Fake News</h3>
            <p>{fakeNews}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default JournalistPage;
