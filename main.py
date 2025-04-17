from database.connection import DBObject
from router.user_router import user_router
from fastapi import FastAPI
import uvicorn

app = FastAPI()
app.include_router(user_router)

@app.on_event("startup")
async def startup():
    await DBObject.init_async_db() 

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)