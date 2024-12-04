from fastapi import APIRouter, Depends
import schemas, models
from typing import List
from database import get_db
from sqlalchemy.orm import Session
from Hashing import Hash
from passlib.context import CryptContext
from Oauth2 import get_current_user



router = APIRouter()



@router.post('/user', tags=['User'])
def create_user(request: schemas.User, db : Session = Depends(get_db)):
    hashedPassword = Hash.bcrypt(request.password)
    new_user = models.User(name = request.name, email = request.email, password = hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/user",  response_model= List[schemas.UserData], tags=['User'])
def getUsers( db : Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    allUser = db.query(models.User).all()
    return allUser

@router.get('/user/{id}', response_model=schemas.UserData, tags=['User'])
def getUser(id: int, db : Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not found")
    return user