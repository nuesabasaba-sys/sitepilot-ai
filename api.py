from fastapi.responses import FileResponse

from pydantic import BaseModel

from fastapi import FastAPI
from analyzer import SiteAnalysis, analyze_site

app = FastAPI()

class AnalyzeRequest(BaseModel):
    url: str


@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.post("/analyze")
def analyze(request: AnalyzeRequest) -> SiteAnalysis:
    return analyze_site(request.url)
