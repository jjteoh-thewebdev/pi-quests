"use client"

import { Canvas } from "@react-three/fiber"
import { OrbitControls } from "@react-three/drei"
import Sun from "./sun"
import Galaxy from "./galaxy"

export default function SunVisualization() {
    return (
        <div className="w-full h-full">
            <Canvas data-testid="sun-visualizer" camera={{ position: [0, 20, 30], fov: 45, far: 1000 }}
                gl={{
                    powerPreference: "high-performance",
                    antialias: true,
                    failIfMajorPerformanceCaveat: true,
                }}>
                <Galaxy />

                <ambientLight intensity={0.5} />
                <pointLight position={[10, 10, 10]} intensity={1} />
                <Sun onClick={() => { }} />
                <OrbitControls
                    enableZoom={true}
                    enablePan={false}
                    minDistance={1}
                    maxDistance={60}
                    autoRotate
                    autoRotateSpeed={0.5}
                />
            </Canvas>
        </div>
    )
}
