import math

class OrderProcessor:
    def __init__(self, warehouses, vehicle_manager):
        self.warehouses = warehouses
        self.vehicle_manager = vehicle_manager

    def process_order(self, order_id, product_id, quantity, delivery_address):
        # Step 1: Find the closest warehouse with enough stock
        warehouse = self.find_closest_warehouse(product_id, quantity, delivery_address)
        if warehouse:
            # Step 2: Check if there is a delivery vehicle available
            vehicle = self.vehicle_manager.allocate_vehicle(quantity)
            if vehicle:
                # Step 3: Deduct stock from warehouse and complete the order
                warehouse.remove_item(product_id, quantity)
                print(f"Order {order_id} processed. Vehicle {vehicle.vehicle_id} will deliver {quantity} of {product_id} to {delivery_address}.")
                # Release vehicle after delivery
                self.vehicle_manager.release_vehicle(vehicle, quantity)
                return True
            else:
                print(f"No vehicle available for order {order_id}.")
                return False
        else:
            print(f"Order {order_id} failed. No warehouse has sufficient stock.")
            return False

    def find_closest_warehouse(self, product_id, quantity, delivery_address):
        min_distance = float('inf')
        closest_warehouse = None
        for warehouse in self.warehouses:
            if warehouse.has_stock(product_id, quantity):
                # Calculate distance to the delivery address (simple Euclidean distance)
                distance = self.calculate_distance(delivery_address, warehouse)
                if distance < min_distance:
                    min_distance = distance
                    closest_warehouse = warehouse
        return closest_warehouse

    def calculate_distance(self, delivery_address, warehouse):
        x1, y1 = map(int, delivery_address.split())  # Assume delivery_address is "x y"
        x2, y2 = map(int, warehouse.warehouse_id.split())  # Assume warehouse coordinates as "x y"
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
