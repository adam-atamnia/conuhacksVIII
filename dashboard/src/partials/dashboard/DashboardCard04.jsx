import React from "react";
import { BarChart } from "@mui/x-charts/BarChart";

function DashboardCard04({ numberOfCarsWithTypes }) {
  return (
    <div className="flex flex-col col-span-full sm:col-span-6 bg-white dark:bg-slate-800 shadow-lg rounded-sm border border-slate-200 dark:border-slate-700">
      <header className="px-5 py-4 border-b border-slate-100 dark:border-slate-700">
        <h2 className="font-semibold text-slate-800 dark:text-slate-100">
          Number of vehicles serviced and turned away per type
        </h2>
      </header>
      <BarChart
        dataset={numberOfCarsWithTypes}
        series={[
          { dataKey: "missedCount", label: "Turned away", color: "#C7D2FE" },
          { dataKey: "servedCount", label: "Serviced", color: "#4F46E5" },
        ]}
        height={500}
        xAxis={[
          {
            dataKey: "type",
            scaleType: "band",
          },
        ]}
        margin={{ top: 40, bottom: 40, left: 40, right: 10 }}
      />
    </div>
  );
}

export default DashboardCard04;
