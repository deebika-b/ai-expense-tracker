from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import users, expenses, ai


Base.metadata.create_all(bind=engine)


app = FastAPI()


# Allow React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router)
app.include_router(expenses.router)
app.include_router(ai.router)


@app.get("/")
def root():
    return {"message": "AI Expense Tracker API"}