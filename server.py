import base64
import grpc
import warehouse_pb2
import warehouse_pb2_grpc
import order_pb2
import order_pb2_grpc
from concurrent import futures
import logging

import math
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from Crypto.Random import get_random_bytes


class WareHouseServicer(warehouse_pb2_grpc.WarehouseServiceServicer):
    def warehouseLocation(self, request, context):
        coordinates = []
        with open("./files/warehouse.txt", "r") as f:
            for line in f:
                values = line.split()
                coordinates.append(warehouse_pb2.Location.Tuple(x=values[0], y=values[1]))
        return warehouse_pb2.Location(coordinates=coordinates)


class OrderServicer(order_pb2_grpc.OrderServiceServicer):
    # def __init__(self, vehicles):
    #     self.vehicles = vehicles

    def processOrder(self, request, context):
        order_id = request.order_id
        product_id = request.product_id
        quantity = request.quantity
        delivery_address = request.delivery_address

        # Skip the decryption logic and just return the order details directly
        order = self.process_order(order_id, product_id, quantity, delivery_address)
        
        # Allocate the order to the warehouse
        allocated_warehouse = self.allocate_warehouse(order)

        if allocated_warehouse:
            return order_pb2.OrderResponse(success=True, message=f"Order {order_id} processed and assigned to warehouse at coordinates {allocated_warehouse}.")
        else:
            return order_pb2.OrderResponse(success=False, message=f"Failed to process order {order_id}. No available warehouse.")

    def process_order(self, order_id, product_id, quantity, delivery_address):
        # Directly return the order details without any encryption or decryption
        print(f"Processing order: {order_id} for product: {product_id}, quantity: {quantity}, delivery to: {delivery_address}")
        return {"order_id": order_id, "product_id": product_id, "quantity": quantity, "delivery_address": delivery_address}

    def allocate_warehouse(self, order):
        # Check if any warehouse can fulfill the order (simplified logic for now)
        with open("./files/warehouse.txt", "r") as f:
            for line in f:
                values = line.split()
                # Simple logic: if warehouse coordinates match the delivery address, assign the order
                if self.check_proximity(order['delivery_address'], values):
                    return values
        return None

    def check_proximity(self, delivery_address, warehouse_coordinates):
        # Calculate Euclidean distance between delivery address and warehouse coordinates
        x1, y1 = map(int, delivery_address.split())  # Assume delivery_address is in "x y" format
        x2, y2 = map(int, warehouse_coordinates)
        
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        # Define a threshold distance for proximity (e.g., 5 units)
        if distance <= 5:
            return True
        return False


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # Add services to the server
    warehouse_pb2_grpc.add_WarehouseServiceServicer_to_server(WareHouseServicer(), server)
    order_pb2_grpc.add_OrderServiceServicer_to_server(OrderServicer(), server)

    server.add_insecure_port('[::]:50052')
    print("Server started...")
    server.start()
    logging.basicConfig()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
