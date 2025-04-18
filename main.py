from controller.request_controller import request_controller
from controller.reward_controller import reward_controller
from controller.review_controller import review_controller
from controller.match_controller import match_controller
from controller.user_controller import user_controller
from database.connection import DBObject
from fastapi import FastAPI
import uvicorn

app = FastAPI()
app.include_router(user_controller)
app.include_router(request_controller)
app.include_router(match_controller)
app.include_router(review_controller)
app.include_router(reward_controller)

@app.on_event("startup")
async def startup():
    await DBObject.init_async_db() 

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)