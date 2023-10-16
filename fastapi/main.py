import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse
from pydantic import BaseModel
from sqlcoder.mytest import return_response
from sqlcoder.inference import run_inference
from sqlcoder import inference
import subprocess
import requests

app = FastAPI()
db=[]
#----------------------------------------------------------------------------------------------------------
# data models

class City(BaseModel):
    name: str
    timezone: str

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/sqlcoder", StaticFiles(directory="sqlcoder"), name="sqlcoder")

#app.include_router(index.router);

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/sql")
def sqlcoder(request: Request):
    context = {"request": request}
    return templates.TemplateResponse('sql.html',context)


class Item(BaseModel):
    question:str
    
        

@app.post("/apitest")
def apitest(item:Item):
    question = item.question
    
    
    #return question


    #result = subprocess.check_output(["python", "sqlcoder/inference.py", "-q", question], text=True, stderr=subprocess.STDOUT)
    result = run_inference(question)
    return {"query": question, "result": result}
    
@app.post("/apitest2")
def apitest2(item:Item):
    question = item.question
    
    
    return question


    


@app.get("/apitest")
def apitest():
    
    return "ok"


# @app.route("/sql_generation", method=['POST'])
# def generation():
    





@app.get("/cities", response_class=HTMLResponse)
def get_cities(request: Request):
    context = {}
    rsCity = []

    cnt = 0
    for city in db:
        str=f"http://worldtimeapi.org/api/timezone/{city['timezone']}"
        print(str)
        r = requests.get(str)
        cur_time = r.json()['datetime']

        cnt += 1
        rsCity.append({'id': cnt, 'name':city['name'], 'timezone': city['timezone'], 'current_time': cur_time})

    context['request'] = request
    context['rsCity'] = rsCity

    return templates.TemplateResponse('city_list.html', context)

@app.get('/cities/{city_id}')
def get_city(city_id: int):
    city = db[city_id-1]
    r = requests.get(f"http://worldtimezpi.org/api/timezone/{city['timezone']}")
    cur_time = r.json()['datetime']
    return {'name': city['name'], 'timezone': city['timezone'], 'current_time': cur_time}

@app.post('/cities')
def create_city(city: City):
    db.append(city.dict())
    return db[-1]

@app.delete('/cities/{city_id}')
def delete_city(city_id: int):
    db.pop(city_id-1)
    return {}


if __name__ == '__main__':
    uvicorn.run(app)