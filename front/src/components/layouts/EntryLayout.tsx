import { Outlet } from "react-router";

function entryLayout(){
    return (
        <div className="flex flex-col items-center justify-center h-screen p-25 bg-stone-200">
            <Outlet/>
        </div>
    )
}

export default entryLayout