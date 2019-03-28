from concurrent import futures
import time
import logging
import grpc

import sliceable_transceiver_sdm_service_pb2
import sliceable_transceiver_sdm_service_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class TransceiverService(sliceable_transceiver_sdm_service_pb2_grpc.TransceiverServiceServicer):
    def __init__(self):
        self.transceiver = sliceable_transceiver_sdm_service_pb2.transceiver()

    def SetTransceiver(self, request, context):
        logging.debug("Received transceiver " + str(request))
        #self.transceiver.connection.extend([request])
        return sliceable_transceiver_sdm_service_pb2.empty()
 
    def GetBer (self, request, context):
        logging.debug("Get Ber")
        ber=sliceable_transceiver_sdm_service_pb2.ber(ber=10)
        yield ber


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sliceable_transceiver_sdm_service_pb2_grpc.add_TransceiverServiceServicer_to_server(TransceiverService(), server)
    server.add_insecure_port('[::]:50051')
    logging.debug("Starting server")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    serve()
