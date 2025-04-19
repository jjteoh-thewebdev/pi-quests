"use client"

import { useRef } from "react"
import { Canvas, useFrame } from "@react-three/fiber"
import { OrbitControls, Environment, useTexture } from "@react-three/drei"
import type { Mesh } from "three"
import Sun from "./sun"
import Galaxy from "./galaxy"

export default function SunVisualization() {
    return (
        <div className="w-full h-full">
            <Canvas camera={{ position: [0, 20, 30], fov: 45, far: 1000 }}
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

// function Sun() {
//     const meshRef = useRef<Mesh>(null)
//     const sunTexture = useTexture("/textures/2k_sun.jpg")

//     // Apply a yellow/orange color to make it look like the sun
//     useFrame((state, delta) => {
//         if (meshRef.current) {
//             meshRef.current.rotation.y += delta * 0.1
//         }
//     })

//     return (
//         <mesh ref={meshRef}>
//             <sphereGeometry args={[1, 64, 64]} />
//             <meshStandardMaterial map={sunTexture} emissive={"#ff7b00"} emissiveIntensity={0.5} />
//         </mesh>
//     )
// }
