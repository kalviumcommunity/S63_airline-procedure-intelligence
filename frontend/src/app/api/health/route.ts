import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    status: 'healthy',
    service: 'skyops-frontend',
    timestamp: new Date().toISOString(),
    environment: process.env.NEXT_PUBLIC_APP_ENV || 'development',
  });
}

