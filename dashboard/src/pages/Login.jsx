import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';


const LoginPage = () => {
  const { loginWithRedirect, isAuthenticated } = useAuth0();

  return ( !isAuthenticated &&
    <div className="flex h-screen bg-gray-100">
      <div className="m-auto text-center">
        <h1 className="text-4xl font-bold text-indigo-600 mb-4">Welcome to Our Dashboard!</h1>
        <p className="text-lg text-gray-700 mb-8">Click the button below to get started.</p>
        <button
          onClick={() => loginWithRedirect({ redirect_uri: "http://localhost:5173/upload" })}
          className="bg-indigo-500 hover:bg-indigo-600 text-white font-bold py-2 px-4 rounded"
        >
          {!isAuthenticated ? <div>Login</div>: <div>Logout</div>}
        </button>
        
      </div>
    </div>
  );
};

export default LoginPage;
