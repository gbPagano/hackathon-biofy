from fastapi import FastAPI

from src.routes.webhook import wb_app

app = FastAPI()
app.include_router(wb_app)


@app.get("/")
def root():
    return {"Hello": "World"}
