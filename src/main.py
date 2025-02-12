import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

main_app = FastAPI()


@main_app.get('/')
def start(request: Request):
    return templates.TemplateResponse('start.html', {'request': request})


@main_app.get('/ai_search')
def search_ai(request: Request):
    return templates.TemplateResponse('search.html', {'request': request})


if __name__ == "__main__":
    uvicorn.run("main:main_app")
