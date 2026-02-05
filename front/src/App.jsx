import React from "react";
import { Outlet } from "react-router";

import AppSidebar from "./components/AppSidebar";

export default function App() {
  return (
    <div className="flex ">
      <div>
        <AppSidebar />
      </div>

      <section className="bg-red-100 flex-1 h-[300vh]">
        <p>Helloooo</p>
        <Outlet />
      </section>
    </div>
  );
}
