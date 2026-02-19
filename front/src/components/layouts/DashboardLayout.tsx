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
                        {/* <div className="grid auto-rows-min gap-4 md:grid-cols-3">
                            <div className="bg-muted/50 aspect-video rounded-xl" />
                            <div className="bg-muted/50 aspect-video rounded-xl" />
                            <div className="bg-muted/50 aspect-video rounded-xl" />
                        </div>
                        <div className="bg-muted/50 min-h-[100vh] flex-1 rounded-xl md:min-h-min" /> */}
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
