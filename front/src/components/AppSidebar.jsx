import React from 'react'
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarHeader,
  SidebarFooter,
} from "@/components/ui/sidebar";
import { useNavigate } from 'react-router';
import { Home, UserCog } from 'lucide-react';

const main_items = [
  {
      title: "Home",
      url: "",
      icon: Home
  },
  {
      title: "User Profile",
      url: "profile",
      icon: UserCog
  },
  {
    title: "Books",
    url: "books",
    icon: UserCog
},
]

export default function AppSidebar() {
  const nav = useNavigate()
  const currentPage = useLocation().pathname
  const logout = () => {
      localStorage.clear()
      navigate("/")
  }

  return (
    <Sidebar>
      <SidebarHeader>
        Online Reading Platform
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>
            Menu
          </SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {
                main_items.map((item) => (
                    <SidebarMenuItem key={item.title}>
                        <SidebarMenuButton asChild isActive={item.url === currentPage}>

                            <Link to={item.url}>
                                <item.icon />
                                <span>{item.title}</span>
                            </Link>
                        </SidebarMenuButton>
                    </SidebarMenuItem>
                ))
              }
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <div className="flex flex-col w-full">
            <Button variant="destructive" onClick={logout}>
                Logout
            </Button>
        </div>
      </SidebarFooter>
    </Sidebar>
  )
}
