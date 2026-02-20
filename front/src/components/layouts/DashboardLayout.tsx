import { Outlet } from "react-router";
// import StickyHeader from "../custom-components/mainHeader";
import { Footer7 } from "../custom-components/mainFooter";
import { AppSidebar } from "@/components/custom-components/app-sidebar"
import { SiteHeader } from "@/components/custom-components/site-header"
import {
    SidebarInset,
    SidebarProvider,
} from "@/components/ui/sidebar"

function dashLayout() {
    return (
        <div className="[--header-height:calc(--spacing(14))]">
        <SidebarProvider className="flex flex-col">
            <SiteHeader />
            <div className="flex flex-1">
                <AppSidebar />
                <SidebarInset className="">
                    <div className="flex flex-1 flex-col gap-4 min-h-screen">
                        
                        <Outlet/>
                    <Footer7 />
                    </div>
                </SidebarInset>
            </div>
        </SidebarProvider>
        </div>
    );
}

export default dashLayout;
