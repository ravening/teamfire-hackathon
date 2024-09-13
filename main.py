from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import backend.aimodel.chat as chat
import logging
import requests
import cosmos
from customerdata import populate_customer_data
from conversation import chat_with_ai


customer_data = ''

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    print('Request for index page received')
    return templates.TemplateResponse('index.html', {"request": request})


@app.get("/chat", response_class=HTMLResponse)
async def index(request: Request):
    print('Request for index page received')
    return templates.TemplateResponse('chat.html', {"request": request})


@app.get("/read")
async def index(request: Request):
    logger.error('Request for read all items received')
    return cosmos.data()


@app.get("/customer/{id}")
async def get_customer_by_id(id: str):
    global customer_data
    logger.error('Fetching customer details')
    response = cosmos.get_customer_by_id(id=id)
    customer_data = response[0]
    populate_customer_data(response[0])
    return response


@app.get('/favicon.ico')
async def favicon():
    file_name = 'favicon.ico'
    file_path = './static/' + file_name
    return FileResponse(path=file_path, headers={'mimetype': 'image/vnd.microsoft.icon'})


@app.post('/hello', response_class=HTMLResponse)
async def hello(request: Request, name: str = Form(...)):
    global customer_data
    if name:
        name = chat_with_ai("unique_conversation_id", name)
        return templates.TemplateResponse('hello.html', {"request": request, 'name':name})
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return RedirectResponse(request.url_for("index"), status_code=status.HTTP_302_FOUND)


@app.post('/chatresponse')
async def chatresponse(request: Request, name: str = Form(...)):
    if name:
        response = chat.chat_with_ai(name)
        return response
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return RedirectResponse(request.url_for("index"), status_code=status.HTTP_302_FOUND)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)

