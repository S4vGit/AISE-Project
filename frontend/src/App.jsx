import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import AdminPage from './pages/AdminPage';
import ResearcherPage from './pages/ResearcherPage';
import JournalistPage from './pages/JournalistPage';
import { jwtDecode } from 'jwt-decode';


const App = () => {
  const [user, setUser] = useState(null);

  // Retrieve the user from the token stored in local storage
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      const decoded = jwtDecode(token);
      setUser({ user_id: decoded.sub, role: decoded.role });
    }
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/admin" element={user?.role === 'A' ? <AdminPage /> : <Home />} />
        <Route path="/researcher" element={user?.role === 'R' ? <ResearcherPage /> : <Home />} />
        <Route path="/journalist" element={user?.role === 'J' ? <JournalistPage /> : <Home />} />
      </Routes>
    </Router>
  );
};

//

export default App;
