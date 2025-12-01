import React from 'react'
import { Outlet } from 'react-router'
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/AppSidebar"

export default function MainLayout() {
  return (
    <SidebarProvider>
    <AppSidebar/>
        <SidebarTrigger />
          <main className="w-full">
              <div className="flex flex-col items-center justify-center p-5">
                <Outlet />
              </div>
          </main>
    </SidebarProvider>
  )
}
