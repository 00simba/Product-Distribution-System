# Product-Distribution-System

Setup Project On Visual Studio Code:

1. Clone this repository
2. Open a terminal in the project directory and type the following commands
3. pip install virtualenv
4. virtualenv venv
5. source venv/bin/activate
6. Run the Python file using the Play button. 


After making changes to .proto file run the following and change the protofile in the last argument:

python -m grpc_tools.protoc -I./protos --python_out=. --pyi_out=. --grpc_python_out=. ./protos/warehouse.proto
python -m grpc_tools.protoc -I./protos --python_out=. --pyi_out=. --grpc_python_out=. ./protos/order.proto
