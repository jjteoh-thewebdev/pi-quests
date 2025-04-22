"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import { Check, Copy, HelpCircle, Loader2, RefreshCcw } from "lucide-react"
import {
    Tooltip,
    TooltipContent,
    TooltipProvider,
    TooltipTrigger,
} from "@/components/ui/tooltip"
import { Button } from "@/components/ui/button"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog"
import { Textarea } from "./ui/textarea"


const SUN_RADIUS_KM = 695700
const KM_TO_MILES = 0.621371

export default function SunInfo() {
    const [pi, setPi] = useState<string>("3.14159265358979323846")
    const [unit, setUnit] = useState<"km" | "miles">("km")
    const [loading, setLoading] = useState<boolean>(false)
    const [refreshing, setRefreshing] = useState<boolean>(false)
    const [dp, setDp] = useState<number>(0)
    const [hasError, setHasError] = useState<boolean>(false)

    const [modalOpen, setModalOpen] = useState(false)
    const [copied, setCopied] = useState(false)


    useEffect(() => {
        fetchPi()
    }, [])

    const fetchPi = async () => {
        setLoading(true)

        try {
            const response = await fetch("/api/pi")

            if (!response.ok) throw new Error("Error fetching pi")

            const data: { pi: string, dp: string } = await response.json()
            setPi(data.pi)
            setDp(Number(data.dp))
        } catch (error) {
            console.error("Error fetching pi:", error)
            setHasError(true)
        } finally {
            setLoading(false)
            setRefreshing(false)
        }
    }

    const getLatestPi = async () => {
        setHasError(false)
        setModalOpen(true)
        await fetchPi()

    }

    const calculateCircumference = (): string => {
        const piValue = pi ? Number.parseFloat(pi.substring(0, 12)) : 3.14159265 // takes 3.{10 digits} as JS Number don't deal well with high precision
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

    const copyToClipboard = () => {
        navigator.clipboard.writeText(pi)
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
    }

    return (
        <>
            <Card className="h-full gap-4">
            <CardHeader>
                    <CardTitle className="flex items-center justify-between border-b pb-2">
                        <h3 className="text-xl font-bold">Sun Information</h3>

                    <div className="flex items-center justify-end space-x-2 pt-2">
                        <Label htmlFor="unit-toggle">km</Label>
                            <Switch id="unit-toggle" data-testid="unit-toggle" className="cursor-pointer" checked={unit === "miles"} onCheckedChange={toggleUnit} />
                        <Label htmlFor="unit-toggle">miles</Label>
                    </div>
                </CardTitle>
            </CardHeader>
                <CardContent className="space-y-6">
                <div>
                        <h3 className="text-lg font-medium mb-2">Formula of Circumference:</h3>
                    <p className="text-2xl font-semibold">
                        C = 2πr
                    </p>
                </div>

                <div>
                        <h4 className="flex items-center text-md font-medium mb-2 mr-1">
                            <span className="mr-1">Pi(π)</span>
                            <TooltipProvider>
                                <Tooltip>
                                    <TooltipTrigger asChild>
                                        <HelpCircle
                                            data-testid="info-icon"
                                            className="w-3 h-3 text-blue-500 cursor-pointer"
                                            onClick={() => getLatestPi()} />
                                    </TooltipTrigger>
                                    <TooltipContent>
                                        <p>View more precise value of Pi(π)</p>
                                    </TooltipContent>
                                </Tooltip>
                            </TooltipProvider>
                        </h4>


                        <p className="text-md font-semibold">
                        3.14159265
                    </p>
                </div>

                <div>
                        <h4 className="text-md font-medium mb-2">Radius(r)</h4>
                        <p className="text-md font-semibold" data-testid="radius">
                        {unit === "km"
                            ? `${SUN_RADIUS_KM.toLocaleString()} km`
                            : `${(SUN_RADIUS_KM * KM_TO_MILES).toLocaleString(undefined, { maximumFractionDigits: 2 })} miles`}
                    </p>
                </div>

                <div>
                    <h3 className="text-lg font-medium mb-2">Circumference</h3>
                    <p className="text-2xl font-semibold" data-testid="circumference">
                        {calculateCircumference()} {unit}
                    </p>
                </div>

                <div>
                    <h3 className="text-lg font-medium mb-2">Other Facts</h3>
                    <ul className="list-disc pl-5 space-y-1 text-slate-700 dark:text-slate-300">
                        <li>Surface temperature: 5,500°C (9,940°F)</li>
                        <li>Age: ~4.6 billion years</li>
                        <li data-testid="distance-from-earth">Distance from Earth: {unit === "km" ? "~150 million km" : "~93 million miles"}</li>
                    </ul>
                </div>


            </CardContent>
        </Card>

            <Dialog open={modalOpen} onOpenChange={setModalOpen}>
                <DialogContent className="sm:max-w-md">
                    {loading && !refreshing ?
                        (<>
                            <DialogHeader>
                                <DialogTitle>Loading Pi Value</DialogTitle>
                            </DialogHeader>
                            <div className="flex items-center gap-2 py-4">
                                <Loader2 className="h-4 w-4 animate-spin text-blue-500" />
                                <span>Fetching Pi(π) from server...</span>
                            </div>
                        </>) :
                        hasError ?
                            (<>
                                <DialogHeader>
                                    <DialogTitle>Error</DialogTitle>
                                </DialogHeader>
                                <div className="space-y-4 py-4">
                                    <p className="text-red-500">Error fetching pi. Please try again later.</p>
                                </div>
                            </>)
                            : (<>
                                <DialogHeader>
                                    <DialogTitle>Value of Pi(π)</DialogTitle>
                                    <DialogDescription>Showing value of Pi(π) to {dp} decimal places.</DialogDescription>
                                </DialogHeader>
                                <div className="space-y-4 py-4">
                                    <Textarea className="font-mono h-60 resize-none" readOnly value={pi} style={{ wordBreak: "break-all" }} />


                                    <div className="flex justify-end gap-2">
                                        <Button onClick={() => {
                                            setRefreshing(true)
                                            fetchPi()
                                        }} className="flex items-center gap-2 bg-blue-500 hover:bg-blue-600 text-white">
                                            {
                                                refreshing ?
                                                    <><Loader2 className="h-4 w-4 animate-spin" /> Refreshing...</> :
                                                    <><RefreshCcw className="h-4 w-4" /> Refresh</>
                                            }

                                        </Button>
                                        <Button onClick={copyToClipboard} className="flex items-center gap-2">
                                            {copied ? (
                                                <>
                                                    <Check className="h-4 w-4" />
                                                    Copied!
                                                </>
                                            ) : (
                                                <>
                                                    <Copy className="h-4 w-4" />
                                                    Copy to Clipboard
                                                </>
                                            )}
                                        </Button>
                                    </div>
                                </div>
                            </>)
                    }
                </DialogContent>
            </Dialog >

        </>
    )
}
