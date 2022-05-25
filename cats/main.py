from typing import List

from fastapi import FastAPI, Response, Request, Depends, Body, Form, Path
from starlette.responses import FileResponse

from schema import Out, In
from crud import create_cats, get_all, find_cat, edit_item, delete_cat

app = FastAPI()


@app.get('/', response_class=FileResponse)
async def index():
    return FileResponse(path='templates/index.html')


@app.post('/cats/cats')
def create_item(name: str = Form(...), breed: str = Form(...), age: int = Form(...)):
    print(name, breed, age, sep='\n')
    # cat = create_cats(date.dict())
    # url = f'http://127.0.0.1:8000/cats/cats/{cat.id}'
    # return Out(name=cat.name, breed=cat.breed, age=cat.age, url=url)


@app.get('/cats/cats')
async def view_all():
    cats = get_all()
    return cats


@app.post('/cats/cats/{id}')
async def edit_cat(id: int = Path(...), name: str = Form(...), breed: str = Form(...), age: int = Form(...)):
    data = {'name': name, 'breed': breed, 'age': age}
    cat = find_cat(id)
    print(cat)
    if cat is not None:
        print('Base edited' if edit_item(cat, data) else 'Error')
    else:
        print("Cat don't found")


@app.delete('/cats/cats/{id}')
async def edit_cat(id: int = Path(...)):
    print('Done' if delete_cat(id) else 'Error deleting')


