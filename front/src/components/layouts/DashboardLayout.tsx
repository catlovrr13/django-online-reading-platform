import { Outlet } from "react-router";

function dashLayout(){
    return (
        <div className="flex flex-col items-center justify-center min-h-screen p-4 sm:p-6 lg:p-8 ">
            <Outlet/>
        </div>
    )
}

export default dashLayout