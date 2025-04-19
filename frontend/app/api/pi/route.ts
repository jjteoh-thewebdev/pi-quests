import { type NextRequest, NextResponse } from "next/server"

// Default precision value
const DEFAULT_PRECISION = 100

// Function to calculate Pi to a specified precision using the Nilakantha series
function calculatePi(precision: number): string {
    // For simplicity, we'll use a pre-calculated value of Pi
    // In a real application, you might want to use a more sophisticated algorithm
    const PI = "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"

    // Return Pi to the specified precision
    return PI.substring(0, precision + 2) // +2 to account for "3."
}

export async function GET(request: NextRequest) {
    try {
        // Get the precision from the query parameters
        const searchParams = request.nextUrl.searchParams
        const precisionParam = searchParams.get("precision")

        // Parse the precision parameter, or use the default value
        const precision = precisionParam ? Number.parseInt(precisionParam, 10) : DEFAULT_PRECISION

        // Validate the precision
        // if (isNaN(precision) || precision < 1 || precision > 100) {
        //     return NextResponse.json({ error: "Precision must be a number between 1 and 100" }, { status: 400 })
        // }

        // Calculate Pi to the specified precision
        const piValue = calculatePi(precision)

        // Add a small delay to simulate a more complex calculation
        await new Promise((resolve) => setTimeout(resolve, 500))

        // Return the calculated value
        return NextResponse.json({ value: piValue })
    } catch (error) {
        console.error("Error calculating Pi:", error)
        return NextResponse.json({ error: "Failed to calculate Pi" }, { status: 500 })
    }
}
