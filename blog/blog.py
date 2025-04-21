from fastapi import FastAPI,Response
from typing import Optional
from blog.schemas import Blog
from fastapi import status
from minio import Minio
import logs

appBlog = FastAPI()

@app.get('/blog')
def index(limit = 10, published: bool = True, sort: Optional[str] = None):
    logs.logger.info("checking if published is True or False")
    if published:
        return {'data':f'{limit} published blogs from db'}
    else:
        return {'data':f'{limit} blogs from db'}
    

@app.get('/blog/unpublished')
def unpublished():
    logs.logger.info("returning all unpublished blogs")
    return {'data':'all unpublished blogs'}

@app.get('/blog/{id}')
def show(id: int):
    # fetch blog with id = id
    return {'data': id}

@app.get('/blog/{id}/comments')
def comments(id):
    #fetch comments blog with id = id
    return {'data':{'1','2'}}


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(created_blog: Blog):
    logs.logger.info("creating a blog")
    return {'data': f"blog is created with the title {created_blog.title}"}