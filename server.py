import grpc
import warehouse_pb2
import warehouse_pb2_grpc
from concurrent import futures
import logging

class WareHouseServicer(warehouse_pb2_grpc.WarehouseServiceServicer):
    def warehouseLocation(self, request, context):
        coordinates = []
        with open("./files/warehouse.txt", "r") as f:
            for line in f:
                values = line.split()
                coordinates.append(warehouse_pb2.Location.Tuple(x=values[0], y=values[1]))

        return warehouse_pb2.Location(coordinates=coordinates)


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    warehouse_pb2_grpc.add_WarehouseServiceServicer_to_server(WareHouseServicer(), server)
    print("Server Started")
    logging.basicConfig()
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

main()