import React, { useState } from 'react';

import Sidebar from '../partials/Sidebar';
import Header from '../partials/Header';
import WelcomeBanner from '../partials/dashboard/WelcomeBanner';

import { FileInput, Label } from 'flowbite-react';
import { Toast } from 'flowbite-react';
import { HiFire } from 'react-icons/hi';


async function do2tasks(){
    
    await new Promise(resolve => setTimeout(resolve, 500));
    <Toast>
      <div className="inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-cyan-100 text-cyan-500 dark:bg-cyan-800 dark:text-cyan-200">
        <HiFire className="h-5 w-5" />
      </div>
      <div className="ml-3 text-sm font-normal">Set yourself free.</div>
      <Toast.Toggle />
    </Toast>
    
}

function UploadFile() {

  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [showToast, setShowToast] = useState(false);

  const handleFileUpload = async () => {
    await new Promise(resolve => setTimeout(resolve,500));

    setShowToast(true);

    setTimeout(() => setShowToast(false), 2500);
  }

  return (
    <div className="flex h-screen overflow-hidden">

      {/* Sidebar */}
      <Sidebar sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />
     
      {/* Content area */}
      <div className="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden">

        {/*  Site header */}
        <Header sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

        <main>
          <div className="px-4 sm:px-6 lg:px-8 py-8 w-full max-w-9xl mx-auto">

            {/* Welcome banner */}
            <WelcomeBanner />

            {/* Dashboard actions */}
            <div className="sm:flex sm:justify-between sm:items-center mb-8">
            
            <div className="flex w-full items-center justify-center">
                        <Label
                            htmlFor="dropzone-file"
                            className="dark:hover:bg-bray-800 flex h-64 w-full cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-300 bg-gray-50 hover:bg-gray-100 dark:border-gray-600 dark:bg-gray-700 dark:hover:border-gray-500 dark:hover:bg-gray-600"
                        >
                            <div className="flex flex-col items-center justify-center pb-6 pt-5">
                            <svg
                                className="mb-4 h-8 w-8 text-gray-500 dark:text-gray-400"
                                aria-hidden="true"
                                xmlns="http://www.w3.org/2000/svg"
                                fill="none"
                                viewBox="0 0 20 16"
                            >
                                <path
                                stroke="currentColor"
                                strokeLinecap="round"
                                strokeLineJoin="round"
                                strokeWidth="2"
                                d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
                                />
                            </svg>
                            <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
                                <span className="font-semibold">Click to upload</span> or drag and drop
                            </p>
                            <p className="text-xs text-gray-500 dark:text-gray-400">.csv accepted</p>
                            </div>
                            <FileInput id="dropzone-file" className="hidden" onChange={handleFileUpload}/>

                        </Label>
            </div>
            
            </div>
            {showToast && (
              <div className="fixed bottom-4 right-4 z-50 w-64">
              <Toast >
                <div className="inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-cyan-100 text-cyan-500 dark:bg-cyan-800 dark:text-cyan-200">
                  <HiFire className="h-5 w-5" />
                </div>
                <div className="ml-3 text-sm font-normal">File uploaded successfully.</div>
                <Toast.Toggle />
              </Toast>
            </div>
            )}

          </div>
        </main>

        {/* <Banner /> */}

      </div>
    </div>
  );
}

export default UploadFile;
