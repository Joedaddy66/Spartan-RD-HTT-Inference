from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .launchpad import launchpad_config
from .codex_connectors.wolfram_adapter import eval_wolfram

app = FastAPI(title="CodexHub API", version=launchpad_config["system_config"]["codex_version"])


class NameRequest(BaseModel):
    name: str

@app.post("/")
def greet_user(req: NameRequest):
    return {"message": f"Hello, {req.name}"}


class EvaluationRequest(BaseModel):
    expression: str
    phrase: str = "codexhub"
    seed_n: str = "sha256:codex-default"
    deterministic: bool = True
    context_vars: dict = {}

@app.get("/health")
def health():
    return {
        "status": "SFC: PASS",
        "codex_version": launchpad_config["system_config"]["codex_version"]
    }

@app.post("/api/v1/evaluate")
def evaluate(req: EvaluationRequest):
    if not req.expression:
        raise HTTPException(status_code=400, detail="Expression is mandatory.")
    out = eval_wolfram(
        phrase=req.phrase,
        expression=req.expression,
        seed_n=req.seed_n,
        deterministic=req.deterministic,
        context_vars=req.context_vars,
        engine_path=launchpad_config["wolfram_connector"]["engine_path"],
        timeout_s=launchpad_config["wolfram_connector"]["default_expression_timeout"]
    )
    if out["status"] != "PASS":
        raise HTTPException(status_code=500, detail=f"Connector failed: {out['trace_log']}")
    if out["RA_score"] < launchpad_config["system_config"]["ra_threshold"]:
        raise HTTPException(status_code=500, detail="RA score below threshold")
    return {"status": "PASS", "data": out["result"], "ra_proof": out["proof"], "ra_score": out["RA_score"]}
