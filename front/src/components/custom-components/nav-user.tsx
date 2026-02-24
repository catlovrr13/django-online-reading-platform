"use client"

import {
  BadgeCheck,
  Bell,
  ChevronsUpDown,
  CreditCard,
  LogOut,
  Sparkles,
  LogIn
} from "lucide-react"

import {
  Avatar,
  AvatarFallback,
  AvatarImage,
} from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar"

import { useDispatch } from "react-redux"
import { useCookies } from "react-cookie"
import { reset } from "@/hooks/redux/slice"
import { useNavigate } from "react-router"

export function NavUser({
  user,
}: {
  user: {
    username: string
    token: string
    refresh: string
    first_name?: string
    last_name?: string
    email?: string
    subscription_type?: string
  } | null
}) {
  const { isMobile } = useSidebar()
  const nav = useNavigate()

  const displayName = user?.first_name || user?.last_name
    ? `${user.first_name} ${user.last_name}`
    : user?.username || "Guest"
  const avatarFallback = (user?.first_name?.charAt(0) || user?.username?.charAt(0) || "G").toUpperCase()

  const [_, , removeCookie] = useCookies(["token"])
  const dispatch = useDispatch()

  const handleLogout = () => {
    removeCookie("token")
    dispatch(reset())
    nav("/")
  }

  const handleLogin = () => {
    nav("/")
  }

  const handleUpgrade = () => {
    nav("/subscription")
  }

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <SidebarMenuButton
              size="lg"
              className="data-[state=open]:bg-sidebar-accent data-[state-open]:text-sidebar-accent-foreground"
            >
              <Avatar className="h-8 w-8 rounded-lg">
                <AvatarImage src="" alt={displayName} />
                <AvatarFallback className="rounded-lg">{avatarFallback}</AvatarFallback>
              </Avatar>
              <div className="grid flex-1 text-left text-sm leading-tight">
                <span className="truncate font-medium">{displayName}</span>
                <span className="truncate text-xs">{user?.username || ""}</span>
              </div>
              <ChevronsUpDown className="ml-auto size-4" />
            </SidebarMenuButton>
          </DropdownMenuTrigger>
          <DropdownMenuContent
            className="w-(--radix-dropdown-menu-trigger-width) min-w-56 rounded-lg"
            side={isMobile ? "bottom" : "right"}
            align="end"
            sideOffset={4}
          >
            <DropdownMenuLabel className="p-0 font-normal">
              <div className="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
                <Avatar className="h-8 w-8 rounded-lg">
                  <AvatarImage src="" alt={displayName} />
                  <AvatarFallback className="rounded-lg">{avatarFallback}</AvatarFallback>
                </Avatar>
                <div className="grid flex-1 text-left text-sm leading-tight">
                  <span className="truncate font-medium">{displayName}</span>
                  <span className="truncate text-xs">{user?.username || ""}</span>
                </div>
              </div>
            </DropdownMenuLabel>
            {user?.subscription_type === 'free-365'? (
              <>
                <DropdownMenuSeparator />
                <DropdownMenuGroup>
                  <DropdownMenuItem onSelect={handleUpgrade}>
                    <Sparkles />
                    Upgrade to Premium
                  </DropdownMenuItem>
                </DropdownMenuGroup>
              </>
            ) : (
              <>
              <DropdownMenuSeparator />
                <DropdownMenuGroup>
                  <DropdownMenuItem onSelect={handleLogin}>
                    <LogIn />
                    Log in / Sign up
                  </DropdownMenuItem>
                </DropdownMenuGroup>
              </>
            )}
            <DropdownMenuSeparator />
              {displayName === "Guest" ? (null) : 
              <>
            <DropdownMenuGroup>
              <DropdownMenuItem>
                <BadgeCheck />
                Account
                </DropdownMenuItem>
              {user?.subscription_type === 'premium-30' || user?.subscription_type === 'premium-365' ? (
                <>
              <DropdownMenuItem>
                <CreditCard />
                Billing
              </DropdownMenuItem>
                </>
              ) : null}
              <DropdownMenuItem>
                <Bell />
                Notifications
              </DropdownMenuItem>
            </DropdownMenuGroup>
            <DropdownMenuSeparator />
            <DropdownMenuItem onSelect={handleLogout}>
              <LogOut />
              Log out
            </DropdownMenuItem>
              </>
              }
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarMenuItem>
    </SidebarMenu>
  )
}
