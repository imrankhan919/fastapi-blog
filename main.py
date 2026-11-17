from fastapi import FastAPI , Depends , HTTPException
from sqlmodel import SQLModel, Session, select
from sqlalchemy.exc import OperationalError 
from database import engine , get_session
from models import Blog

app = FastAPI()

@app.on_event("startup")
def on_startup():
    try:
        SQLModel.metadata.create_all(engine)
        print("Database Connected Successfully!")
    except OperationalError as e:
        print("Database Connection Failed:", e)



@app.get("/")
def home() : 
    return {"message" : "WELCOME TO BLOG API 1.0"}



@app.post("/blog")
def create_blog(blog : Blog ,  session: Session = Depends(get_session)) : 
    session.add(blog)
    session.commit()
    session.refresh(blog)
    return blog


@app.get("/blogs")
def get_blogs(session: Session = Depends(get_session)) : 
    return session.exec(select(Blog)).all()

@app.get("/blog/{blog_id}")
def get_blog(blog_id: int ,session: Session = Depends(get_session)) : 
    blog = session.get(Blog , blog_id)
    if not blog :
        raise HTTPException(status_code=404 , detail="Blog Not Found")
    return blog

@app.put("/blog/{blog_id}")
def update_blog(blog_id: int , update : Blog ,  session: Session = Depends(get_session)) : 
    blog = session.get(Blog , blog_id)
    if not blog :
        raise HTTPException(status_code=404 , detail="Blog Not Found")
    blog.title = update.title 
    blog.description = update.description 
    blog.author = update.author 
    blog.is_published = update.is_published
    blog.words = update.words 
    session.add(blog) 
    session.commit()
    session.refresh(blog)
    return blog



@app.delete("/blog/{blog_id}")
def remove_blog(blog_id: int ,  session: Session = Depends(get_session)) : 
    blog = session.get(Blog , blog_id)
    if not blog :
        raise HTTPException(status_code=404 , detail="Blog Not Found")
    session.delete(blog) 
    session.commit()
    return {"message" : "Blog Removed!"}
