import React, { useState } from "react";

import Sidebar from "../partials/Sidebar";
import Header from "../partials/Header";
import WelcomeBanner from "../partials/dashboard/WelcomeBanner";
import Datepicker from "../components/Datepicker";
import DashboardCard01 from "../partials/dashboard/DashboardCard01";
import DashboardCard02 from "../partials/dashboard/DashboardCard02";
import DashboardCard04 from "../partials/dashboard/DashboardCard04";

import DashboardCard08 from "../partials/dashboard/DashboardCard08";
import DashboardCard09 from "../partials/dashboard/DashboardCard09";

import { TailSpin } from "react-loader-spinner";
import { calculations } from "../utils/functions";
import { Toast } from "flowbite-react";
import { IoIosWarning } from "react-icons/io";

function Dashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [selectedDates, setSelectedDates] = useState({
    startDate: null,
    endDate: null,
  });
  const [totalRevenue, setTotalRevenue] = useState(1000);
  const [missedRevenue, setMissedRevenue] = useState(200);
  const [showToast, setShowToast] = useState(false);
  const [numberOfCarsWithTypes, setNumberOfCarsWithTypes] = useState([
    { type: "compact", servedCount: 0, missedCount: 0 },
    { type: "medium", servedCount: 0, missedCount: 0 },
    { type: "full-size", servedCount: 0, missedCount: 0 },
    { type: "class 1 truck", servedCount: 0, missedCount: 0 },
    { type: "class 2 truck", servedCount: 0, missedCount: 0 },
  ]);

  const fetchData = async () => {
    if (selectedDates.startDate && selectedDates.endDate) {
      const formattedStartDate = selectedDates.startDate
        .toISOString()
        .split("T")[0];
      const formattedEndDate = selectedDates.endDate
        .toISOString()
        .split("T")[0];

      const url = `https://httpsflask-p653ixf4wq-uc.a.run.app/stats/get_data?start_date=${formattedStartDate}&end_date=${formattedEndDate}`;

      try {
        document.getElementById("page").classList.add("hidden");
        document.getElementById("spinner").classList.remove("hidden");
        document.getElementById("spinner").classList.add("flex");
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        console.log(data);
        document.getElementById("page").classList.remove("hidden");
        document.getElementById("spinner").classList.add("hidden");
        document.getElementById("spinner").classList.remove("flex");
        setTotalRevenue(calculations(data)[0]);
        setMissedRevenue(calculations(data)[1]);
        setNumberOfCarsWithTypes(calculations(data)[2]);
      } catch (error) {
        console.error("Fetch error:", error);
      }
    } else {
      console.log("Start or end date is missing");
      setShowToast(true);
      setTimeout(() => setShowToast(false), 3000);
    }
  };

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
              {/* Right: Actions */}
              <div className="grid grid-flow-col sm:auto-cols-max justify-start sm:justify-end gap-2">
                <Datepicker
                  onDateChange={(startDate, endDate) =>
                    setSelectedDates({ startDate, endDate })
                  }
                />

                {/* Add view button */}
                <button
                  className="btn bg-indigo-500 hover:bg-indigo-600 text-white"
                  onClick={fetchData}
                >
                  <svg
                    className="w-4 h-4 fill-current opacity-50 shrink-0"
                    viewBox="0 0 16 16"
                  >
                    <path d="M15 7H9V1c0-.6-.4-1-1-1S7 .4 7 1v6H1c-.6 0-1 .4-1 1s.4 1 1 1h6v6c0 .6.4 1 1 1s1-.4 1-1V9h6c.6 0 1-.4 1-1s-.4-1-1-1z" />
                  </svg>
                  <span className="hidden xs:block ml-2">Generate</span>
                </button>
              </div>
            </div>

            {showToast && (
              <div className="fixed top-[5rem] right-4 z-50 w-64 ">
                <Toast className="bg-red-100">
                  <div className="inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-red-500 dark:bg-cyan-800 dark:text-cyan-200">
                    <IoIosWarning className="h-5 w-5" />
                  </div>
                  <div className="ml-3 text-sm font-extrabold">
                    Choose a date range first!
                  </div>
                  <Toast.Toggle className="bg-red-100 hover:bg-transparent" />
                </Toast>
              </div>
            )}
            {/* Spinner */}
            <div
              id="spinner"
              className="pt-12 items-center justify-center hidden"
            >
              <TailSpin color="#4F46E5" height={400} width={400} radius="1" />
            </div>
            {/* Cards */}
            <div id="page">
              {/* Line chart (Acme Plus) */}
              <div className="grid grid-cols-2 gap-6">
                <DashboardCard01
                  totalRevenue={totalRevenue.toLocaleString("en-US")}
                />

                {/* Line chart (Acme Advanced) */}
                <DashboardCard02
                  missedRevenue={missedRevenue.toLocaleString("en-US")}
                />
              </div>

              <div className="grid grid-cols-2 gap-6 my-4 ">
                {/* Bar chart (Direct vs Indirect) */}
                <DashboardCard04
                  numberOfCarsWithTypes={numberOfCarsWithTypes}
                />
                {/* Line chart (Sales Over Time) */}
                {/* <DashboardCard08 /> */}
                {/* Stacked bar chart (Sales VS Refunds) */}
                {/* <DashboardCard09 /> */}
              </div>
            </div>
          </div>
        </main>

        {/* <Banner /> */}
      </div>
    </div>
  );
}

export default Dashboard;
