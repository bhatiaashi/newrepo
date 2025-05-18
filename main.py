from contextlib import asynccontextmanager
from typing import Annotated, Sequence

import uvicorn
from fastapi import Depends, FastAPI, status, HTTPException
from sqlmodel import Session, SQLModel, select
from starlette.responses import Response


from database import my_engine
from models import Blog

def get_session():
    with Session(my_engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app : FastAPI):
    SQLModel.metadata.create_all(my_engine)
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/blog",status_code=status.HTTP_201_CREATED)
def create_blog(blog: Blog, session: SessionDep) -> Blog:
    session.add(blog)
    session.commit()
    session.refresh(blog)
    return blog

@app.get("/blog")
def get_blog( session: SessionDep , limit : int = 10) -> Sequence[Blog]:
    # list of Row objects
    # Select * from Blog : ORM - Object Relational Model
    rows = session.exec(select(Blog).limit(limit)).all()
    return rows

@app.get("/blog/{id_blog}")
def get_blog( response : Response , session: SessionDep,id_blog : int) -> Blog:
    # list of Row objects
    row = session.exec(select(Blog).filter(Blog.id == id_blog)).first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"Blog with {id_blog} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail":f"Blog with {id_blog} not found"}
    return row
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info")
