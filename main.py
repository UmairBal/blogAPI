from fastapi import FastAPI, Depends
import schemas
from database import Base, engine

from routers import authentication, blog, user
from Oauth2 import get_current_user


app = FastAPI()

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)

@app.delete("/delete-all-tables", tags=["Danger"])
def delete_all_tables(current_user: schemas.User = Depends(get_current_user)):
    Base.metadata.drop_all(bind=engine)
    return {"message": "All tables have been deleted"}

