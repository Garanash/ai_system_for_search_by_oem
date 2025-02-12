import uvicorn
from fastapi import FastAPI


main_app = FastAPI()

@main_app.get('/')
def hello_world():
    return {'success': "true"}


if __name__ == "__main__":
    uvicorn.run("main:main_app")