from fastapi import FastAPI
from uvicorn import run
from database import db_conn
from models.all import Base
from router import auth, roler, permissioner, cityer, facilitier, mediaer

Base.metadata.create_all(db_conn.engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(roler.router)
app.include_router(permissioner.router)
app.include_router(cityer.router)
app.include_router(facilitier.router)
app.include_router(mediaer.router)



if __name__ == '__main__':  
    run("main:app", reload=True)
