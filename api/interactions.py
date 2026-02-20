from fastapi import FastAPI, Request, HTTPException
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import os

app = FastAPI()
PUBLIC_KEY = os.getenv("DISCORD_PUBLIC_KEY")

@app.post("/api/interactions")
async def interactions(request: Request):
    signature = request.headers.get("X-Signature-Ed25519")
    timestamp = request.headers.get("X-Signature-Timestamp")
    body = await request.body()

    # Discord Validation Handshake
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
    try:
        verify_key.verify(f'{timestamp}{body.decode()}'.encode(), bytes.fromhex(signature))
    except BadSignatureError:
        raise HTTPException(status_code=401, detail="invalid request signature")

    return {"type": 1} # PING response
