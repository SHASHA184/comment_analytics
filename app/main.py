from fastapi import FastAPI
from routers import auth, post, comment
import uvicorn

app = FastAPI()

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(comment.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
