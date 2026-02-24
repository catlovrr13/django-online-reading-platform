"use client"

import bmarkdark from "@/assets/media/bmarkdark.svg"
import bmarklight from "@/assets/media/bmarklight.svg"

import { SearchForm } from "@/components/custom-components/search-form"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import { useSidebar } from "@/components/ui/sidebar"

import { useTheme } from '@/components/theme-provider'
import { ThemeToggle } from "../theme-toggle"

export function SiteHeader() {
  const { toggleSidebar, state } = useSidebar()
  const isSidebarOpen = state === 'expanded'

  const { theme } = useTheme()
  const currentLogo = theme === 'dark' ? bmarklight : bmarkdark

  return (
    <header className="bg-background sticky top-0 z-50 flex w-full items-center border-b">
      <div className="flex h-(--header-height) w-full items-center gap-3 px-3">
        <Button
          className="h-8 w-8 hover:-translate-y-0.5"
          variant="ghost"
          size="icon"
          onClick={toggleSidebar}
        >
          <img
            src={currentLogo}
            alt='theonyxpub.'
            className={`transition-transform duration-300 ease-in-out ${isSidebarOpen ? '-rotate-90' : ''}`}
            />
        </Button>
        <Separator orientation="vertical" className="mr-2 h-4" />
        <Breadcrumb className="hidden sm:block">
          <BreadcrumbList>
            <BreadcrumbItem>
              <BreadcrumbLink href="#">Home</BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator />
            <BreadcrumbItem>
              <BreadcrumbPage>Dashboard</BreadcrumbPage>
            </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>
        <ThemeToggle/>
        <SearchForm className="w-full sm:ml-auto sm:w-auto" />
      </div>
    </header>
  )
}
