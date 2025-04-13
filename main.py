from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from blog.schemas import Blog
import logs



app = FastAPI()

@app.get('/blog')
def index(limit = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {'data':f'{limit} published blogs from db'}
    else:
        return {'data':f'{limit} blogs from db'}
    

@app.get('/blog/unpublished')
def unpublished():
    return {'data':'all unpublished blogs'}

@app.get('/blog/{id}')
def show(id: int):
    # fetch blog with id = id
    return {'data': id}

@app.get('/blog/{id}/comments')
def comments(id):
    #fetch comments blog with id = id
    return {'data':{'1','2'}}


@app.post('/blog')
def create_blog(created_blog: Blog):
    return {'data': f"blog is created with the title {created_blog.title}"}