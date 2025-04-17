from controller.user_controller import user_controller
from database.connection import DBObject
from fastapi import FastAPI
import uvicorn

app = FastAPI()
app.include_router(user_controller)

@app.on_event("startup")
async def startup():
    await DBObject.init_async_db() 

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)