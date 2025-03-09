from threading import Lock

class VehicleManager:
    def __init__(self, num_vehicles):
        self.num_vehicles = num_vehicles
        self.lock = Lock()

    def allocate_vehicle(self):
        with self.lock:
            if self.num_vehicles > 0:
                self.num_vehicles -= 1
                return True
            else:
                return False

    def release_vehicle(self):
        with self.lock:
            self.num_vehicles += 1