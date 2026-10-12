from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel

from fastapi import FastAPI
from analyzer import SiteAnalysis, analyze_site

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class AnalyzeRequest(BaseModel):
    url: str


@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.post("/analyze")
def analyze(request: AnalyzeRequest) -> SiteAnalysis:
    return analyze_site(request.url)
