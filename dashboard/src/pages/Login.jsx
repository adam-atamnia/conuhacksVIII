import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';


const LoginPage = () => {
  const { loginWithRedirect } = useAuth0();

  return (
    <div className="flex h-screen bg-gray-100">
      <div className="m-auto text-center">
        <h1 className="text-4xl font-bold text-indigo-600 mb-4">Welcome to Our Dashboard!</h1>
        <p className="text-lg text-gray-700 mb-8">Click the button below to log in and get started.</p>
        <button
          onClick={() => loginWithRedirect()}
          className="bg-indigo-500 hover:bg-indigo-600 text-white font-bold py-2 px-4 rounded"
        >
          Login
        </button>
        
      </div>
    </div>
  );
};

export default LoginPage;
