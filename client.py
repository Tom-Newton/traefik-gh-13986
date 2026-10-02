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


def create_local_channel() -> grpc.Channel:
    return grpc.insecure_channel("localhost:50051")


def create_remote_channel() -> grpc.Channel:
    return grpc.secure_channel(
        f"{os.environ['HOST']}:443", grpc.ssl_channel_credentials()
    )


def main() -> None:
    create_channel = (
        create_remote_channel if "HOST" in os.environ else create_local_channel
    )
    with create_channel() as channel:
        stub = stream_pb2_grpc.TerminatingStreamStub(channel)
        responses = stub.Stream(requests())
        for response in responses:
            print(response)


if __name__ == "__main__":
    main()
