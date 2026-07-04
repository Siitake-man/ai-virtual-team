from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import projects, employees, chat

app = FastAPI(
    title="AI Virtual Team Builder API",
    version="1.0.0"
)

# CORS configuration to allow requests from Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(projects.router)
app.include_router(employees.router)
app.include_router(chat.router)

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok", "message": "API server is running"}
