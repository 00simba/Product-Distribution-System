# class DeliveryTruck:
#     def __init__ (self, range, active):
#         self.range = range
#         self.active = active

from threading import Lock
import time

class DeliveryTruck:
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.is_available = True
        self.lock = Lock()  # Mutex lock for vehicle availability

    def allocate_vehicle(self):
        """Try to acquire the vehicle, blocking until available."""
        with self.lock:
            if self.is_available:
                self.is_available = False
                print(f"Vehicle {self.vehicle_id} allocated.")
                return True
            else:
                print(f"Vehicle {self.vehicle_id} is currently in use.")
                return False

    def release_vehicle(self):
        """Release the vehicle after delivery is done."""
        with self.lock:
            self.is_available = True
            print(f"Vehicle {self.vehicle_id} is now available.")

