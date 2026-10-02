FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    grpcio==1.84.0 \
    protobuf==7.35.1

COPY server.py stream_pb2.py stream_pb2_grpc.py ./

CMD ["python", "server.py"]
