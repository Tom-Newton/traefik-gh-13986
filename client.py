"""Client for the bidirectional stream termination example."""

import os
import time
from collections.abc import Iterator

import grpc

import stream_pb2
import stream_pb2_grpc


def requests() -> Iterator[stream_pb2.StreamMessage]:
    yield stream_pb2.StreamMessage(data=b"test")
    time.sleep(1000)  # Prevent the client to server stream from closing during the test
    yield stream_pb2.StreamMessage(data=b"test2")

def main() -> None:
    if os.environ.get("K3D", "false")== "true":
        host="localhost:80"
    else:
        host="localhost:50051"
    with grpc.insecure_channel(host) as channel:
        stub = stream_pb2_grpc.TerminatingStreamStub(channel)
        responses = stub.Stream(requests())
        for response in responses:
            print(response)


if __name__ == "__main__":
    main()
