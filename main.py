from database.connection import DBObject
from router.user_router import user_router
from fastapi import FastAPI
import uvicorn

app = FastAPI()
DBObject.init_async_db()
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)