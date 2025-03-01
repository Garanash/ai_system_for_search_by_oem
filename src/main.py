import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from core.config import settings

templates = Jinja2Templates(directory='templates')

main_app = FastAPI()


@main_app.get('/')
def start(request: Request):
    return templates.TemplateResponse('start.html', {'request': request})


@main_app.get('/ai_search')
def search_ai(request: Request):
    return templates.TemplateResponse('search.html', {'request': request, "userdata": None})


@main_app.get('/ai_finded')
def finded_ai(request: Request):
    return templates.TemplateResponse('finded.html', {'request': request, "userdata": None})


if __name__ == "__main__":
    uvicorn.run("main:main_app",
                host=settings.run.host,
                port=settings.run.port,
                reload=True,
                )
