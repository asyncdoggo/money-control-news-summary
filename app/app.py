from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.moneycontrolextractor import MoneyControlExtractor


app = FastAPI()

extractor = MoneyControlExtractor()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/news-list")
async def get_news_list(page: int):
    return extractor.get_news_list(page)

@app.post("/news-content")
async def get_news_content(request: Request):
    data = await request.json()
    link = data["link"]
    return {"content": extractor.get_news_content(link)}

