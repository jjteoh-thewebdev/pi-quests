import { NextResponse } from 'next/server';

export async function GET() {
    try {
        const baseUrl = process.env.API_BASE_URL;
        const apiKey = process.env.API_KEY;

        if (!baseUrl || !apiKey) {
            return NextResponse.json(
                { error: 'Missing API configuration' },
                { status: 500 }
            );
        }

        const response = await fetch(`${baseUrl}/api/pi`, {
            method: 'GET',
            headers: {
                'x-api-key': apiKey,
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            return NextResponse.json(
                { error: `API responded with status: ${response.status}` },
                { status: response.status }
            );
        }

        const data = await response.json();
        return NextResponse.json(data, { status: 200 });
    } catch (error) {
        console.error('Error fetching pi value:', error);
        return NextResponse.json(
            { error: 'Failed to fetch pi value' },
            { status: 500 }
        );
    }
}
