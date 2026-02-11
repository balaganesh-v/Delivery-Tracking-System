from utils.email import send_registration_email, send_login_otp_email , send_email_to_driver
from utils.security import hash_password, verify_password, generate_otp
from repositories.admin_repository import AdminRepository

# Temporary OTP storage (use Redis in production)
OTP_STORE = {}

class AdminService:
    def __init__(self, repo: AdminRepository):
        self.repo = repo
    
    def admin_register(self, username, email, password):
        if self.repo.get_by_email(email):
            return None

        hashed = hash_password(password)
        admin = self.repo.create_admin(username, email, hashed)
        send_registration_email(email, username)
        return admin

    def admin_login(self, email, password):
        admin = self.repo.get_by_email(email)
        if not admin:
            return None
        if not verify_password(password, admin.password):
            return None
        otp = generate_otp()
        OTP_STORE[email] = otp
        send_login_otp_email(email, otp)
        return admin

    def verify_otp(self, email, otp):
        stored_otp = OTP_STORE.get(email)
        if not stored_otp or stored_otp != otp:
            return None
        OTP_STORE.pop(email)
        admin = self.repo.get_by_email(email)
        return admin
    
    def get_all_drivers(self):
        return self.repo.get_all_drivers()
    
    def add_new_driver(self,name, email, phone, vehicle_number, password):
        hashed = hash_password(password)
        driver = self.repo.create_driver(name, email, phone, vehicle_number, hashed)
        send_email_to_driver(email, name,password)
        return driver
        
    def get_all_orders(self):
        return self.repo.get_all_orders()
    
    def get_available_orders(self):
        return self.repo.get_available_orders()
    
    def assign_order_to_driver(self, order_id: int, driver_id: int):
        # Check if order exists
        order = self.repo.get_order_by_id(order_id)
        if not order:
            return None, "Order not found"

        # Check if driver exists
        driver = self.repo.get_driver_by_id(driver_id)
        if not driver:
            return None, "Driver not found"

        # Check if order is already assigned
        if self.repo.is_order_assigned(order_id):
            return None, "Order already assigned"

        # Assign order
        assignment = self.repo.create_order_assignment(order_id, driver_id)

        # Update order status
        self.repo.update_order_status(order_id, "ASSIGNED")

        return assignment, None
    
    def get_ordered_assignments(self):
        return self.repo.get_all_order_assignments()
    
    def get_latest_updates(self):
        return self.repo.get_latest_updates()
