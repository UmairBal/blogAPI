from fastapi import  APIRouter, status, Depends, Response
import schemas
from typing import List
from database import get_db
from sqlalchemy.orm import Session
import Oauth2
import models
from Oauth2 import get_current_user


router = APIRouter()


@router.post("/blog", status_code=status.HTTP_201_CREATED, tags=['Blog'])
def createBlog(request: schemas.Blog, db : Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.delete("/blog/{id}",  status_code = status.HTTP_204_NO_CONTENT, tags=['Blog'])
def deletePost(id, db : Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    
    blog.delete(synchronize_session = False)
    db.commit()
    return "done"

@router.put("/blog/{id}", status_code = status.HTTP_202_ACCEPTED, tags=['Blog'])
def update(id, request: schemas.Blog, db : Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    
    blog.update(request.dict())
    db.commit()
    return 'updated'
    

@router.get("/blog", response_model= List[schemas.ShowBlog], tags=['Blog'])
def getBlogs(db : Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    allBlogs = db.query(models.Blog).all()
    return allBlogs

@router.get('/blog/{id}', status_code=200, tags=['Blog'])
def getSingleBlog(id, response: Response, db : Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"blog with {id} is not available")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"details": f"blog with {id} is not available"}
    return blog
