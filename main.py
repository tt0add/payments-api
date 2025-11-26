from fastapi import FastAPI
from router import router as payments_router
import database.models
from database.db import Base, engine

app = FastAPI(title='Payments API')
app.include_router(payments_router)

Base.metadata.create_all(engine)