"use client"

import { useMemo } from "react"
import * as THREE from "three"
import { useMobile } from "@/hooks/use-mobile"
import { useOptimizedTexture } from "@/hooks/use-optimized-texture"

export default function Galaxy() {
    const isMobile = useMobile()

    // Create optimized geometry
    const geometry = useMemo(() => {
        const segments = isMobile ? [20, 15] : [60, 40]
        return new THREE.SphereGeometry(500, segments[0], segments[1])
    }, [isMobile])

    // Use optimized texture loading
    const texture = useOptimizedTexture('/textures/2k_stars.jpg')

    return (
        <mesh geometry={geometry}>
            <meshBasicMaterial map={texture} side={THREE.BackSide} />
        </mesh>
    )
} 