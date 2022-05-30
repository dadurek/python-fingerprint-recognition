import uvicorn
from fastapi import FastAPI
from routes import router as api_router

app = FastAPI()

origins = ["http://localhost:8000"]

app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, log_level="info", reload=True)
