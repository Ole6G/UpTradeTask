from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from app.models import ClientRequest, ClientReport
from app.services import generate_report

app = FastAPI()


@app.post("/create-report", response_model=ClientReport)
async def create_report(request: ClientRequest):
    report = await generate_report(request)

    if report is None:
        raise HTTPException(status_code=403, detail="Доступ запрещен")

    return report
