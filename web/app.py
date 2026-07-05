from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(title="OKS Suv Web Panel")

templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)


@app.get("/", response_class=HTMLResponse)
async def clients_page(request: Request):
    try:
        from bot.database.connection import async_session
        from bot.database import crud
    except ImportError:
        return HTMLResponse("<h1>Database module not available</h1>")

    async with async_session() as session:
        users = await crud.get_all_users(session)

    return templates.TemplateResponse("clients.html", {"request": request, "users": users})


@app.get("/health")
async def health():
    return {"status": "OK"}
