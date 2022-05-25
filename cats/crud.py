from models import db, Cats


def create_cats(data):
    return Cats.create(**data.dict())


def get_all():
    cats = []
    for y in [x.__data__ for x in Cats.select()]:
        y['url'] = f'http://127.0.0.1:8000/cats/cats/{y["id"]}'
        y.pop('id')
        cats.append(y)
    return cats


def edit_item(cat, newdata):
    try:
        cat.name = newdata['name']
        cat.breed = newdata['breed']
        cat.age = newdata['age']
        cat.save()
        return True
    except:
        return False


def find_cat(id):
    return Cats.get_or_none(id)


def delete_cat(id):
    cat = find_cat(id)
    try:
        cat.delete_instance()
        return True
    except:
        return False


