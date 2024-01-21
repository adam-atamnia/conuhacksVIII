import React, { useEffect } from 'react';
import {
  Routes,
  Route,
  useLocation
} from 'react-router-dom';

import './css/style.css';

import './charts/ChartjsConfig';

// Import pages
import Dashboard from './pages/Dashboard';

import { useAuth0 } from '@auth0/auth0-react';

import UploadFile from './pages/Upload';

function App() {

  const location = useLocation();
  const { loginWithRedirect } = useAuth0();
  const { user, isAuthenticated } = useAuth0();
  

  useEffect(() => {
    document.querySelector('html').style.scrollBehavior = 'auto'
    window.scroll({ top: 0 })
    document.querySelector('html').style.scrollBehavior = ''
  }, [location.pathname]); // triggered on route change

    
  
    
  return (
    <>
      <Routes>
        <Route exact path="/" element={<Dashboard />} />
        <Route exact path="/upload" element={<UploadFile />} />
        
      </Routes>
    </>
  );
}

export default App;
