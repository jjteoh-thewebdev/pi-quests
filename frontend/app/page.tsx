"use client"

import { Suspense } from "react"
import SunVisualization from "@/components/sun-visualization"
import SunInfo from "@/components/sun-info"
import { Loader2 } from "lucide-react"

export default function Home() {
  return (

    <main className="min-h-screen p-4 md:p-8 bg-[#0f172a]  text-white duration-500">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl md:text-5xl font-bold text-center mb-8 text-slate-800 text-white">The Sun</h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-slate-800/80 rounded-lg shadow-lg p-2 h-[500px] md:h-[600px] backdrop-blur-sm">
            <Suspense fallback={<LoadingState />}>
              <SunVisualization />
            </Suspense>
          </div>

          {/* <div className="flex  gap-6"> */}
          <div className="bg-slate-800/80 rounded-lg shadow-lg p-2 backdrop-blur-sm">
            <Suspense fallback={<LoadingState />}>
              <SunInfo />
            </Suspense>
          </div>
          {/* </div> */}
        </div>
      </div>
      </main>
  )
}

function LoadingState() {
  return (
    <div className="flex items-center justify-center h-full">
      <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
      <span className="ml-2 text-slate-600 dark:text-slate-300">Loading...</span>
    </div>
  )
}
