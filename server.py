import time
from collections.abc import Iterator
from concurrent import futures
from threading import Event

import grpc

import stream_pb2, stream_pb2_grpc

LISTEN_ADDRESS = "[::]:50051"


class TerminatingStreamServicer(stream_pb2_grpc.TerminatingStreamServicer):
    def Stream(
        self,
        request_iterator: Iterator[stream_pb2.StreamMessage],
        context: grpc.ServicerContext,
    ) -> Iterator[stream_pb2.StreamMessage]:
        del context
        for input_message in request_iterator:
            print(f"Received: {input_message.data!r}")
            # Need to send at least one message on the server to client stream, in order to reproduce.
            yield stream_pb2.StreamMessage(data=b"response1")
            raise Exception("deliberate failure on the server")
            yield stream_pb2.StreamMessage(data=b"response2")

def main() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    stream_pb2_grpc.add_TerminatingStreamServicer_to_server(TerminatingStreamServicer(), server)
    server.add_insecure_port(LISTEN_ADDRESS)
    server.start()
    print(f"Listening on {LISTEN_ADDRESS}")
    time.sleep(1000)  # Simplest way to keep the server running


if __name__ == "__main__":
    main()
