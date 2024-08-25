from fastapi import FastAPI
from routers import auth
from routers import post
import uvicorn

app = FastAPI()

app.include_router(auth.router)
app.include_router(post.router, prefix="/posts")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
