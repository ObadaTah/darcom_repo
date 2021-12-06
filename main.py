from fastapi import FastAPI
from uvicorn import run
from database import db_conn
from models.all import Base
from router import (
    auth,
    roler,
    permissioner,
    cityer,
    facilitier,
    mediaer,
    producter,
    purchaser,
    packager,
    subscriptioner,
    carder,
    storyer,
    ranker,
    categoryer,
    settinger,
)

Base.metadata.create_all(db_conn.engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(roler.router)
app.include_router(permissioner.router)
app.include_router(cityer.router)
app.include_router(facilitier.router)
app.include_router(producter.router)
app.include_router(purchaser.router)
app.include_router(mediaer.router)
app.include_router(packager.router)
app.include_router(subscriptioner.router)
app.include_router(storyer.router)
app.include_router(carder.router)
app.include_router(ranker.router)
app.include_router(categoryer.router)
app.include_router(settinger.router)


if __name__ == "__main__":
    run("main:app", reload=True)
