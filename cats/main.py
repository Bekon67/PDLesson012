from fastapi import FastAPI, Form, Path, HTTPException, status
from starlette.responses import FileResponse

from schema import Out
from crud import create_cats, get_all, find_cat, edit_item, delete_cat

app = FastAPI()


def prepareOut(cat):
    url = f'http://127.0.0.1:8000/cats/cats/{cat.id}'
    return Out(name=cat.name, breed=cat.breed, age=cat.age, url=url)


@app.get('/', response_class=FileResponse)
async def index():
    return FileResponse(path='templates/index.html')


@app.post('/cats/cats', response_model=Out)
def create_item(name: str = Form(...), breed: str = Form(...), age: int = Form(...)):
    print('Добавлена: ', name, breed, age)
    data = dict(name=name, breed=breed, age=age)
    cat = create_cats(data)
    return prepareOut(cat)


@app.get('/cats/cats')
async def view_all():
    cats = get_all()
    return cats


@app.post('/cats/cats/{id}')
async def edit_cat(id: int = Path(...), name: str = Form(...), breed: str = Form(...), age: int = Form(...)):
    data = {'name': name, 'breed': breed, 'age': age}
    cat = find_cat(id)
    print(cat)
    if cat is not None and edit_item(cat, data):
        print('Запись исправлена')
        return prepareOut(cat)
    else:
        print('Ошибка исправления записи')
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Неправильный адрес кота')


@app.delete('/cats/cats/{id}')
async def edit_cat(id: int = Path(...)):
    return {'result': 'Удаление выполнено' if delete_cat(id) else 'Ошибка удаления'}


