import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

export async function GET() {
  const target = { name: "Prime Medicine", value: 400000 };
  
  try {
    // Sync with Upstash Redis
    await fetch(`${process.env.UPSTASH_REDIS_REST_URL}/incrby/pipeline/${target.value}`, {
      headers: { Authorization: `Bearer ${process.env.UPSTASH_REDIS_REST_TOKEN}` }
    });

    // Notify the Oasis
    await fetch(process.env.DISCORD_WEBHOOK_URL!, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        content: `🔱 **[AUTONOMOUS_HUNT]** Target: ${target.name} | Pipeline: +$${target.value.toLocaleString()}`
      })
    });

    return NextResponse.json({ success: true });
  } catch (err) {
    return NextResponse.json({ success: false, error: "Sync Failed" }, { status: 500 });
  }
}
