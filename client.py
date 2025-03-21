from classes.warehouse import Warehouse
from classes.deliverytruck import DeliveryTruck
from classes.order import Order
import grpc
import warehouse_pb2
import warehouse_pb2_grpc
import order_pb2
import order_pb2_grpc
from google.protobuf import empty_pb2
import math
import threading 

warehouses = []
orders = []

def calculate_distance():
   
   # distance formula d = sqrt((x2 - x1)^2 + (y2 - y1)^2)

   distance = float('inf')

   for warehouse in warehouses:
      for order in orders:

         warehouse_x = float(warehouse.x)
         warehouse_y = float(warehouse.y)

         order_x = float(order.x)
         order_y = float(order.y)

         distance = math.sqrt((warehouse_x - order_x)**2 + (warehouse_y - order_y)**2)

         print(distance)
   
def process_order(x, y, quantity):
   
   print(quantity)
   return 1


def main():

   with grpc.insecure_channel('0.0.0.0:50052') as channel:
      warehouseStub = warehouse_pb2_grpc.WarehouseServiceStub(channel)
      response = warehouseStub.warehouseLocation(warehouse_pb2.Empty())
      for coord in response.coordinates:
        warehouses.append(Warehouse(coord.x, coord.y, capacity=0))

      orderStub = order_pb2_grpc.OrderServiceStub(channel)
      response = orderStub.orderInformation(order_pb2.OrderEmpty())
      for order in response.orderInfo:
         orders.append(Order(order.x, order.y, order.quantity))


if __name__ == '__main__':
   
   main()

   threads = list()

   for order in orders:
      x = threading.Thread(target=process_order, args=(order.x, order.y, order.quantity))
      threads.append(x)
      x.start()

   for thread in threads:
      thread.join()