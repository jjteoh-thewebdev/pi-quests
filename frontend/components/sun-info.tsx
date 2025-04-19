"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import { Loader2 } from "lucide-react"

const SUN_RADIUS_KM = 695700
const KM_TO_MILES = 0.621371

export default function SunInfo() {
    const [pi, setPi] = useState<string>("3.14159265358979323846")
    const [unit, setUnit] = useState<"km" | "miles">("km")
    const [loading, setLoading] = useState<boolean>(false)

    useEffect(() => {
        fetchPi()
    }, [])

    const fetchPi = async () => {
        setLoading(true)
        try {
            const response = await fetch("/api/pi")
            const data = await response.json()
            setPi(data.value)
        } catch (error) {
            console.error("Error fetching pi:", error)
        } finally {
            setLoading(false)
        }
    }

    const calculateCircumference = (): string => {
        const piValue = Number.parseFloat(pi)
        let circumference = 2 * piValue * SUN_RADIUS_KM

        if (unit === "miles") {
            circumference *= KM_TO_MILES
        }

        return circumference.toLocaleString(undefined, {
            maximumFractionDigits: 2,
        })
    }

    const toggleUnit = () => {
        setUnit(unit === "km" ? "miles" : "km")
    }

    return (
        <Card className="h-full">
            <CardHeader>
                <CardTitle className="flex items-center justify-between">
                    <h3 className="text-xl font-bold">Sun Information</h3>
                    {loading && <Loader2 className="h-4 w-4 animate-spin text-blue-500" />}

                    <div className="flex items-center justify-end space-x-2 pt-2">
                        <Label htmlFor="unit-toggle">km</Label>
                        <Switch id="unit-toggle" checked={unit === "miles"} onCheckedChange={toggleUnit} />
                        <Label htmlFor="unit-toggle">miles</Label>
                    </div>
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">

                <div>
                    <h3 className="text-lg font-medium mb-2">Formula of Circumference</h3>
                    <p className="text-2xl font-semibold">
                        C = 2πr
                    </p>
                </div>

                <div>
                    <h3 className="text-lg font-medium mb-2">Pi</h3>
                    <p className="text-2xl font-semibold">
                        3.14159265
                    </p>
                </div>

                <div>
                    <h3 className="text-lg font-medium mb-2">Radius</h3>
                    <p className="text-2xl font-semibold">
                        {unit === "km"
                            ? `${SUN_RADIUS_KM.toLocaleString()} km`
                            : `${(SUN_RADIUS_KM * KM_TO_MILES).toLocaleString(undefined, { maximumFractionDigits: 2 })} miles`}
                    </p>
                </div>

                <div>
                    <h3 className="text-lg font-medium mb-2">Circumference</h3>
                    <p className="text-2xl font-semibold">
                        {calculateCircumference()} {unit}
                    </p>
                </div>

                <div>
                    <h3 className="text-lg font-medium mb-2">Other Facts</h3>
                    <ul className="list-disc pl-5 space-y-1 text-slate-700 dark:text-slate-300">
                        <li>Surface temperature: 5,500°C (9,940°F)</li>
                        <li>Age: ~4.6 billion years</li>
                        <li>Distance from Earth: {unit === "km" ? "~150 million km" : "~93 million miles"}</li>
                    </ul>
                </div>


            </CardContent>
        </Card>
    )
}
