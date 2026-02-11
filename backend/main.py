from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from controllers.admin_controller import router as admin_router
from controllers.driver_controller import router as driver_router
from controllers.websocket_controller import sio

import socketio


# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Delivery Tracking System")

# CORS CONFIGURATION - MUST BE BEFORE ROUTES
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5000",
        "http://127.0.0.1:5000"
    ],
    allow_credentials=True,
    allow_methods=["*"],  # you can just allow all methods if needed
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Include routers AFTER CORS middleware
app.include_router(admin_router)
app.include_router(driver_router)

# Socket.IO mount
socket_app = socketio.ASGIApp(sio)
app.mount("/socket.io", socket_app)

@app.get("/")
def index():
    return {"message": "Backend running successfully"}
