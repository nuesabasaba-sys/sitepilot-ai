from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel, HttpUrl

from fastapi import FastAPI, HTTPException
from analyzer import SiteAnalysis, analyze_site

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

class AnalyzeRequest(BaseModel):
    url: HttpUrl


@app.get("/")
def root():
    return FileResponse("static/index.html")

@app.post("/analyze")
def analyze(request: AnalyzeRequest) -> SiteAnalysis:
    try:
        return analyze_site(str(request.url))

    except TimeoutError as e:
        raise HTTPException(
            status_code=504,
            detail=str(e)
        )
    except ConnectionError as e:
        raise HTTPException(
            status_code=502,
            detail=str(e)
        )
    except RuntimeError as e:
        raise HTTPException(
        status_code=503,
        detail=str(e)
    )