import { Outlet } from "react-router";
import Beams from "../Beams";

function entryLayout() {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen p-4 sm:p-6 lg:p-8 relative">
            <div style={{ position: "absolute", inset: 0, zIndex: 0 }}>
                <Beams
                    beamWidth={2}
                    beamHeight={15}
                    beamNumber={12}
                    lightColor="#ffffff"
                    speed={2}
                    noiseIntensity={1.75}
                    scale={0.2}
                    rotation={0}
                />
            </div>
            <div style={{ position: "relative", zIndex: 1 }}>
                <Outlet />
            </div>
        </div>
        );
}

export default entryLayout;
