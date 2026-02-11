# socketIO/manager.py

class SocketManager:
    def __init__(self):
        # Store more info per driver: driver_id -> { sid, name, email }
        self.connected_users = {}

    def add_user(self, driver_id: str, sid: str, name: str = None, email: str = None):
        self.connected_users[driver_id] = {
            "sid": sid,
            "name": name,
            "email": email,
        }

    def remove_user(self, sid: str):
        for driver_id, info in list(self.connected_users.items()):
            if info["sid"] == sid:
                self.connected_users.pop(driver_id)
                return driver_id
        return None

    def get_sid(self, driver_id: str):
        return self.connected_users.get(driver_id, {}).get("sid")

    def get_info(self, driver_id: str):
        return self.connected_users.get(driver_id)

# Singleton instance
socket_manager = SocketManager()
