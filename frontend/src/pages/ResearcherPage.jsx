import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../assets/style_JR.css';

const ResearcherPage = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [description, setDescription] = useState('');
  const [fakeNews, setFakeNews] = useState('');
  const [fakeProbability, setFakeProbability] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  // Manage the file selection
  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  // Function to detect fake news
  const detectFakeNews = async () => {
    if (!selectedFile) {
      setMessage('Select a file.');
      return;
    }

    // Reset the state
    setDescription('');
    setFakeNews('');
    setFakeProbability('');
    setMessage('Preparing response...');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/detection/detect-fake-news',
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
      setFakeProbability(response.data["fake_probability"]);
      setMessage('');
    } catch (error) {
      setMessage('Error in detecting fake news.');
      console.error(error);
    }
  };

  // Function to handle the logout
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    navigate('/');
  };

  return (
    <div className="journalist-page-container">
      <h2 className="page-title">Researcher Dashboard</h2>

      <button className="logout-button" onClick={handleLogout}>
        Logout
      </button>

      <div className="upload-section">
        <h3>Upload an Image to Detect Fake News</h3>
        <input type="file" onChange={handleFileChange} />
        <button className="generate-button" onClick={detectFakeNews}>Detect</button>
      </div>

      {message && <p className="message">{message}</p>}

      <div className="scrollable-container">
        {description && (
          <div className="output-box">
            <h3>Image Description</h3>
            <p>{description}</p>
          </div>
        )}

        {fakeNews && (
          <div className="output-box">
            <h3>Generated Fake News</h3>
            <p>{fakeNews}</p>
          </div>
        )}

        {fakeProbability && (
          <div className="output-box">
            <h3>Fake News Probability</h3>
            <p>{fakeProbability}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ResearcherPage;
