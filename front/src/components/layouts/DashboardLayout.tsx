import { Outlet } from "react-router";
import StickyHeader from "../custom-components/mainHeader";
import { Footer7 } from "../custom-components/mainFooter";

function dashLayout(){
    return (
        <div className="flex flex-col items-center justify-center">
            <StickyHeader/>
            <Outlet/>
            <Footer7/>
        </div>
    )
}

export default dashLayout