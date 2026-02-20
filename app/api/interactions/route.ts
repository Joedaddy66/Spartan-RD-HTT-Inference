import { NextResponse } from 'next/server';
import nacl from 'tweetnacl';

export async function POST(request: Request) {
  const signature = request.headers.get('x-signature-ed25519');
  const timestamp = request.headers.get('x-signature-timestamp');
  const body = await request.text(); // Get raw body for verification

  // 1. Validate Signature (Crucial for Discord Validation)
  const isVerified = nacl.sign.detached.verify(
    Buffer.from(timestamp + body),
    Buffer.from(signature || '', 'hex'),
    Buffer.from(process.env.DISCORD_PUBLIC_KEY || '', 'hex')
  );

  if (!isVerified) return new Response('Invalid request signature', { status: 401 });

  const data = JSON.parse(body);

  // 2. Handle Discord "Ping"
  if (data.type === 1) return NextResponse.json({ type: 1 });

  // 3. Handle /status Command
  if (data.data?.name === 'status') {
    const redisRes = await fetch(`${process.env.UPSTASH_REDIS_REST_URL}/get/pipeline`, {
      headers: { Authorization: `Bearer ${process.env.UPSTASH_REDIS_REST_TOKEN}` }
    });
    const { result } = await redisRes.json();
    return NextResponse.json({
      type: 4,
      data: { content: `🔱 **[SYSTEM_STATUS]**\nPipeline Milestone: **$${parseInt(result || "0").toLocaleString()}**\nStatus: **NOMINAL**` }
    });
  }

  return NextResponse.json({ type: 4, data: { content: "Acknowledged." } });
}
