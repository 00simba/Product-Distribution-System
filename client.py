from classes.warehouse import Warehouse
from classes.deliverytruck import DeliveryTruck
import grpc
import warehouse_pb2
import warehouse_pb2_grpc
from google.protobuf import empty_pb2

def main():

   with grpc.insecure_channel('0.0.0.0:50052') as channel:
      stub = warehouse_pb2_grpc.WarehouseServiceStub(channel)
      response = stub.warehouseLocation(warehouse_pb2.Empty())
      for coord in response.coordinates:
        print(f"{coord.x} {coord.y}")

if __name__ == '__main__':
   main()