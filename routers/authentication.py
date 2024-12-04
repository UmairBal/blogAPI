from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
import schemas, database, models 
from routers import token
from sqlalchemy.orm import Session
from Hashing import Hash


router = APIRouter(
    tags = [
        "Authentication"
    ]
)

@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    print('USER FOR LOGIN')
    user = db.query(models.User).filter(models.User.email == request.username).first()
    print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid Creadentials")
    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"invalid Password")
    

    access_token = token.create_access_token(
        data={"sub": user.email}
    )
    return schemas.Token(access_token=access_token, token_type="bearer")