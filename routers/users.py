from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/users",
                   responses={404:{"message":"usuario no encontrado"}},
                   tags=["users"]
                   )

#Entidad User
class User(BaseModel):
    id:int
    name:str
    username:str
    social_media:str
    age:int

users_list = [User( id=1,name="Brais",username="Moure", social_media="facebook", age=34),
              User( id=2,name="test", username="test", social_media="instagram", age=34),
             ]

@router.get('/usersjson')
async def usersjson():
    return [{"name":"Luis", "username":"triusdeil", "social_media":"facebook", "age":26},
            {"name":"test", "username":"test", "social_media":"test", "age":26}]

@router.get('/users')
async def users():
    return users_list

#path
@router.get('/user/{id}')
async def user(id: int):
    return search_user(id)


@router.post('/user/',status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204, detail="el usuario ya existe")
    else:
        users_list.append(user)
        return user

@router.put('/user/')
async def user(user:User):
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            return user

@router.delete('/user/{id}')
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    if not found:
        return {"error":"No se ha eliminado el usuario"}

#query
@router.get('/userquery/')
async def user(id: int):
    return search_user(id)
    
def search_user(id:int):
    user = filter(lambda user: user.id == id, users_list)
    try:
        return list(user)[0]
    except:
        return {"error": "no se ha encontrado el usuario"}
