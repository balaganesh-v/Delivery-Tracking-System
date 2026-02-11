# controllers/websocket_controller.py

import socketio
from utils.jwt import decode_access_token
from socketIO.manager import socket_manager
from database import SessionLocal
from models.driver.drivers import Driver  # your ORM model

# Socket.IO server
# Creates Aynchronous Socket.IO server instance
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*"
)

@sio.event
async def connect(sid, environ, auth):
    token = auth.get("token")
    payload = decode_access_token(token)

    if not payload:
        raise ConnectionRefusedError("Unauthorized")

    driver_id = payload["driver_id"]

    # 🔹 Get full driver info from DB
    db = SessionLocal()
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    db.close()

    if not driver:
        raise ConnectionRefusedError("Driver not found")

    # 🔹 Add to SocketManager
    socket_manager.add_user(
        driver_id=driver_id,
        sid=sid,
        name=driver.name,
        email=driver.email
    )

    print(f"✅ {driver_id} connected - {driver.name} ({driver.email})")

@sio.event
async def disconnect(sid):
    driver_id = socket_manager.remove_user(sid)
    if driver_id:
        print(f"🔌 {driver_id} disconnected")
