import { NextRequest, NextResponse } from 'next/server';
import nacl from 'tweetnacl';

// Discord Public Key from Environment Variables
const DISCORD_PUBLIC_KEY = process.env.DISCORD_PUBLIC_KEY;

export async function POST(req: NextRequest) {
  const signature = req.headers.get('x-signature-ed25519') || '';
  const timestamp = req.headers.get('x-signature-timestamp') || '';
  const body = await req.text();

  if (!DISCORD_PUBLIC_KEY) {
    console.error("Missing DISCORD_PUBLIC_KEY in environment variables.");
    return new NextResponse('Internal Server Error', { status: 500 });
  }

  // Verify Discord signature
  const isVerified = nacl.sign.detached.verify(
    new TextEncoder().encode(timestamp + body),
    Buffer.from(signature, 'hex'),
    Buffer.from(DISCORD_PUBLIC_KEY, 'hex')
  );

  if (!isVerified) {
    return new NextResponse('Invalid request signature', { status: 401 });
  }

  const json = JSON.parse(body);

  // Ping command check (Required for Discord handshake)
  if (json.type === 1) {
    return NextResponse.json({ type: 1 });
  }

  // Handle /status command
  if (json.data && json.data.name === 'status') {
    return NextResponse.json({
      type: 4,
      data: { 
        content: '🛡️ **Spartan System Online**\nProject: `clout-estate`\nStatus: [REVENUE_SIGNAL_STAGED]\nMilestone: **$34,450.00**' 
      }
    });
  }

  return NextResponse.json({
    type: 4,
    data: { content: "Command not recognized." }
  });
}
