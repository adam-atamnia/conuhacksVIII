import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router } from 'react-router-dom';
import ThemeProvider from './utils/ThemeContext';
import App from './App';
import { Auth0Provider } from '@auth0/auth0-react';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Router>
    <Auth0Provider
        domain="dev-0nogbpxtep0ie5ct.us.auth0.com"
        clientId="SXp9YpEuY0GI0UkWgduWEaJLwLnda8bN"
        authorizationParams={{
          redirect_uri: "http://localhost:5173/upload"
        }}
      >
      <ThemeProvider>
      
        <App />
      
      </ThemeProvider>
      </Auth0Provider>,
    </Router>
  </React.StrictMode>
);
